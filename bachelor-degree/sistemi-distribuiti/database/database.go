// cpbank - Pagliaroli Chiara 866160 - Piacente Cristian 866020
// Università degli Studi di Milano - Bicocca
// Progetto di Sistemi Distribuiti, A.A 2021-22, Corso di Laurea in Informatica

package database

import (
	"database/sql"
	"errors"
	"fmt"
	"os"

	"gopkg.in/ini.v1"

	_ "github.com/lib/pq"
)

var connection *sql.DB

func getConfiguration() map[string]any {
	ret := make(map[string]any)

	config, err := ini.Load("conf.ini")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to read conf.ini: %v\n", err)
		os.Exit(1)
	}

	section := config.Section("offlineSettings")
	ret["host"] = section.Key("host").String()
	ret["user"] = section.Key("user").String()
	ret["port"] = section.Key("port").String()
	ret["password"] = section.Key("password").String()
	ret["dbname"] = section.Key("dbname").String()

	return ret
}

func Connect() {

	databaseUrl := os.Getenv("DATABASE_URL")

	if len(databaseUrl) == 0 { // offline
		confMap := getConfiguration()

		databaseUrl = fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
			confMap["host"].(string), confMap["port"].(string), confMap["user"].(string), confMap["password"].(string), confMap["dbname"].(string))
	}

	db, err := sql.Open("postgres", databaseUrl)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}

	connection = db
}

func Disconnect() {
	if connection != nil {
		connection.Close()
	}
}

func ExecQuery(query string, args ...any) {
	connection.QueryRow(query, args...)
}

func AddAccount(id string, name string, surname string) {
	connection.QueryRow("INSERT INTO Accounts (id, name, surname) VALUES ($1, $2, $3)", id, name, surname)
}

func countQuery(query string, min_value int, args ...any) bool {
	var count int
	err := connection.QueryRow(query, args...).Scan(&count)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed: %v\n", err)
		Disconnect()
		os.Exit(1)
	}

	return count > min_value
}

func countQueryZero(query string, args ...any) bool { // overloading not supported in golang
	return countQuery(query, 0, args...)
}

func CheckAccountId(id string, active bool) int { // returns 1 if it already exists, 0 if it doesn't, -1 if exists but not active/inactive
	if len(id) != 20 {
		return 0
	}
	foundBool := countQueryZero("SELECT COUNT(id) FROM Accounts WHERE id = $1 AND active = $2", id, active)
	existsBool := countQueryZero("SELECT COUNT(id) FROM Accounts WHERE id = $1", id)
	if foundBool && existsBool {
		return 1
	} else if !foundBool && existsBool {
		return -1
	} else {
		return 0
	}
}

func DeleteAccount(id string, active bool) bool { // returns true if deleted successfully (or doesn't exist)
	// active bool is the current status, it'll be set to the opposite
	if CheckAccountId(id, active) <= 0 { // not found, nothing to delete
		return true
	}
	return countQueryZero("WITH deleted AS (UPDATE Accounts SET active = $1 WHERE id = $2 RETURNING *) SELECT COUNT(*) FROM deleted", !active, id)
}

func GetAllAccounts(active bool) map[string]map[string]string {
	rows, err := connection.Query("SELECT id, name, surname, balance FROM Accounts WHERE active = $1", active)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Query failed in GetAllAccounts: %v\n", err)
		Disconnect()
		os.Exit(1)
	}
	defer rows.Close()

	ret := make(map[string]map[string]string)
	var tmpArr [4]string

	for rows.Next() {
		rows.Scan(&tmpArr[0], &tmpArr[1], &tmpArr[2], &tmpArr[3])
		valuesMap := make(map[string]string)
		valuesMap["name"] = tmpArr[1]
		valuesMap["surname"] = tmpArr[2]
		valuesMap["balance"] = tmpArr[3]
		ret[tmpArr[0]] = valuesMap
	}
	return ret
}

func GetAccountData(id string) map[string]any {
	var accountGeneralData [3]string

	err := connection.QueryRow("SELECT name, surname, balance FROM Accounts WHERE id = $1", id).Scan(&accountGeneralData[0], &accountGeneralData[1], &accountGeneralData[2])
	if err != nil {
		fmt.Fprintf(os.Stderr, "First query failed in GetAccountData: %v\n", err)
		Disconnect()
		os.Exit(1)
	}

	rows, err := connection.Query(`SELECT a.id, a.type, a.idSender, a.idRecipient, a.amount, a.date, 
											CASE WHEN (SELECT COUNT(*) FROM Accounts WHERE id = a.idSender AND active = 't') > 0 THEN 
												't' 
											ELSE 
												'f' 
											END AS senderIsActive,
											CASE WHEN a.idRecipient IS NULL THEN 
												NULL 
											ELSE 
												CASE WHEN (SELECT COUNT(*) FROM Accounts WHERE id = a.idRecipient AND active = 't') > 0 THEN 
													't' 
												ELSE 
													'f' 
												END 
											END AS recipientIsActive
											FROM AccountingOperations a WHERE $1 IN (a.idSender, a.idRecipient) ORDER BY a.date ASC`, id)

	if err != nil {
		fmt.Fprintf(os.Stderr, "Second query failed in GetAccountData: %v\n", err)
		Disconnect()
		os.Exit(1)
	}
	defer rows.Close()

	ret := make(map[string]any) // any can be a string or matrix (for operations)

	ret["name"] = accountGeneralData[0]
	ret["surname"] = accountGeneralData[1]
	ret["balance"] = accountGeneralData[2]

	var operationsMatrix [][2]any

	rowIndex := 0

	var tmpOperationData [5]*string
	var tmpIdsData [2]*bool
	var tmpOperationType int
	for rows.Next() {
		rows.Scan(&tmpOperationData[0], // id
			&tmpOperationType,    // type
			&tmpOperationData[1], // idSender
			&tmpOperationData[2], // idRecipient
			&tmpOperationData[3], // amount
			&tmpOperationData[4], // date
			&tmpIdsData[0],       // senderIsActive
			&tmpIdsData[1])       // recipientIsActive

		fields := [4]string{"idSender", "idRecipient", "amount", "date"}

		operationsMatrix = append(operationsMatrix, [2]any{})

		operationsMatrix[rowIndex][0] = *tmpOperationData[0]
		operationsMatrix[rowIndex][1] = make(map[string]any)

		currentMap := operationsMatrix[rowIndex][1].(map[string]any)

		currentMap["type"] = tmpOperationType

		for i := 0; i < len(fields); i++ {
			if tmpOperationData[i+1] == nil {
				currentMap[fields[i]] = nil
			} else {
				currentMap[fields[i]] = *tmpOperationData[i+1]
			}
		}

		currentMap["senderIsActive"] = *tmpIdsData[0]

		if tmpIdsData[1] == nil {
			currentMap["recipientIsActive"] = nil
		} else {
			currentMap["recipientIsActive"] = *tmpIdsData[1]
		}

		rowIndex++
	}

	ret["operations"] = operationsMatrix

	return ret
}

func HasEnoughMoney(id string, amount float64) bool {
	var balance float64
	err := connection.QueryRow("SELECT balance::numeric::float FROM Accounts WHERE id = $1", id).Scan(&balance)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed in HasEnoughMoney: %v\n", err)
		Disconnect()
		os.Exit(1)
	}
	return balance >= amount
}

func DivertOperation(id string, oldOpData map[string]any) (map[string]string, error) {

	idRecipient := oldOpData["idRecipient"].(*string)
	amount := oldOpData["amount"].(float64)
	if !HasEnoughMoney(*idRecipient, amount) {
		return nil, errors.New("Balance is not sufficient")
	}

	connection.QueryRow("UPDATE AccountingOperations SET type = 4 WHERE id = $1", id)

	idSender := oldOpData["idSender"].(string)
	return DoOperation(3, *idRecipient, &idSender, amount), nil // no error
}

func DoOperation(opType int, idSender string, idRecipient *string, amount float64) map[string]string {
	// idRecipient is a string pointer because it can be nil

	ret := make(map[string]string)

	var uuidv4 string
	var newBalanceSender, newBalanceRecipient string // for opType 0
	var newBalance string                            // for others

	if opType == 0 || opType == 3 { // transfer or cancellation
		connection.QueryRow("UPDATE Accounts SET balance = (balance::numeric::float - $1)::numeric::money WHERE id = $2 RETURNING balance", amount, idSender).Scan(&newBalanceSender)
		connection.QueryRow("UPDATE Accounts SET balance = (balance::numeric::float + $1)::numeric::money WHERE id = $2 RETURNING balance", amount, idRecipient).Scan(&newBalanceRecipient)
	} else { // deposit = 1, withdrawal = 2, can't be 4
		sign := "+"
		if opType == 2 {
			sign = "-"
		}
		connection.QueryRow("UPDATE Accounts SET balance = (balance::numeric::float "+sign+" $1)::numeric::money WHERE id = $2 RETURNING balance", amount, idSender).Scan(&newBalance)
	}

	err := connection.QueryRow("INSERT INTO AccountingOperations (type, idSender, idRecipient, amount) VALUES ($1, $2, $3, $4) RETURNING id", opType, idSender, idRecipient, amount).Scan(&uuidv4)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed in DoOperation: %v\n", err)
		Disconnect()
		os.Exit(1)
	}

	ret["id"] = uuidv4

	if opType != 1 && opType != 2 {
		ret["balanceSender"] = newBalanceSender
		ret["balanceRecipient"] = newBalanceRecipient
	} else {
		ret["balance"] = newBalance
	}

	return ret
}

func UpdateAccountField(id string, newVal string, field string) bool { // true if successful
	var currentVal string
	err := connection.QueryRow("SELECT "+field+" FROM Accounts WHERE id = $1", id).Scan(&currentVal)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed: %v\n", err)
		Disconnect()
		os.Exit(1)
	}
	if currentVal == newVal {
		return true
	}
	return countQueryZero("WITH rows AS (UPDATE Accounts SET "+field+" = $1 WHERE id = $2 RETURNING *) SELECT COUNT(*) FROM rows", newVal, id)
}

func CheckOperationId(id string) bool {
	if len(id) != 36 {
		return false
	}
	return countQueryZero("SELECT COUNT(id) FROM AccountingOperations WHERE id = $1", id)
}

func GetOperationData(id string) map[string]any {
	var opType int
	var idSender string
	var idRecipient *string
	var amount float64

	err := connection.QueryRow("SELECT type, idSender, idRecipient, amount::numeric::float FROM AccountingOperations WHERE id = $1", id).Scan(&opType, &idSender, &idRecipient, &amount)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed in GetOperationData: %v\n", err)
		Disconnect()
		os.Exit(1)
	}

	ret := make(map[string]any)

	ret["opType"] = opType
	ret["idSender"] = idSender
	ret["idRecipient"] = idRecipient
	ret["amount"] = amount

	return ret
}
