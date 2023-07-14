// cpbank - Pagliaroli Chiara 866160 - Piacente Cristian 866020
// Università degli Studi di Milano - Bicocca
// Progetto di Sistemi Distribuiti, A.A 2021-22, Corso di Laurea in Informatica

package handlers

import (
	"cpbank/accounting"
	"cpbank/database"
	jh "cpbank/jsonhelper"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
)

func OnExitHandler() {
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigs
		fmt.Print("Exiting program... ")
		database.Disconnect()
		fmt.Println("Disconnected from database.")
		os.Exit(0)
	}()
}

func NoResourceFound(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, "No resource found", http.StatusNotFound)
}

func noCorrectResourceFound(w http.ResponseWriter, r *http.Request, active bool) { // correct = is active/inactive, depending on the active bool
	tmpStr := ""
	if active {
		tmpStr = "not"
	}
	jh.WriteDataToJSON(w, "Account exists but is "+tmpStr+" active", http.StatusNotFound)
}

func missingParameters(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, "Missing one or more parameters", http.StatusBadRequest)
}

func success(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, "Success!", http.StatusOK)
}

func failed(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, "Failed", http.StatusInternalServerError)
}

func getSingleValue(r *http.Request, field string, rMap map[string]any) string {
	ret := ""
	if r.Header.Get("Content-Type") == "application/json" && rMap != nil {
		if rMap[field] != nil {
			ret = fmt.Sprintf("%v", rMap[field])
		}
	} else {
		ret = r.FormValue(field)
	}
	return ret
}

func deleteAccountHelper(w http.ResponseWriter, r *http.Request, active bool) {
	id := r.URL.Query().Get("id")
	if len(id) == 0 {
		missingParameters(w, r)
	} else {
		deleted := database.DeleteAccount(id, active)
		if deleted {
			success(w, r)
		} else {
			failed(w, r)
		}
	}
}

func getAccountIdHelper(w http.ResponseWriter, r *http.Request, onlyHead bool, active bool) {
	accountId := chi.URLParam(r, "accountId")
	checkAccount := database.CheckAccountId(accountId, active)
	if len(accountId) == 0 || checkAccount <= 0 {
		if onlyHead {
			w.WriteHeader(http.StatusNotFound)
		} else {
			if checkAccount == 0 {
				NoResourceFound(w, r)
			} else {
				noCorrectResourceFound(w, r, active)
			}
		}
	} else {
		accountDataMap := database.GetAccountData(accountId)
		w.Header().Set("X-Sistema-Bancario", fmt.Sprintf("%s;%s", accountDataMap["name"].(string), accountDataMap["surname"].(string)))
		if onlyHead {
			w.WriteHeader(http.StatusOK)
		} else {
			jh.WriteDataToJSON(w, accountDataMap, http.StatusOK)
		}
	}
}

func isValidUUID(u string) bool {
	_, err := uuid.Parse(u)
	return err == nil
}

// endpoints REST

// api/account

func ApiAccountGet(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, database.GetAllAccounts(true), http.StatusOK)
}

func ApiAccountPost(w http.ResponseWriter, r *http.Request) {
	rMap := jh.ReadJSONToMap(r)
	name := getSingleValue(r, "name", rMap)
	surname := getSingleValue(r, "surname", rMap)
	if len(name) == 0 || len(surname) == 0 {
		missingParameters(w, r)
	} else {
		accountId := accounting.NewAccount(name, surname)
		jh.WriteDataToJSON(w, accountId, http.StatusOK)
	}
}

func ApiAccountDelete(w http.ResponseWriter, r *http.Request) {
	deleteAccountHelper(w, r, true)
}

// /api/account/{accountId}

func ApiAccountAccountIdGet(w http.ResponseWriter, r *http.Request) {
	getAccountIdHelper(w, r, false, true)
}

func ApiAccountAccountIdPost(w http.ResponseWriter, r *http.Request) {
	accountId := chi.URLParam(r, "accountId")
	checkAccount := database.CheckAccountId(accountId, true)
	if len(accountId) == 0 || checkAccount <= 0 {
		if checkAccount == 0 {
			NoResourceFound(w, r)
		} else {
			noCorrectResourceFound(w, r, true)
		}
	} else {
		rMap := jh.ReadJSONToMap(r)
		amount := getSingleValue(r, "amount", rMap)

		if len(amount) == 0 {
			missingParameters(w, r)
		} else {
			floatAmount, err := strconv.ParseFloat(amount, 64)
			if err != nil {
				jh.WriteDataToJSON(w, "Failed to parse amount", http.StatusInternalServerError)
			} else {

				opType := 1 // deposit

				if floatAmount < 0 {
					floatAmount = -floatAmount
					if !database.HasEnoughMoney(accountId, floatAmount) {
						jh.WriteDataToJSON(w, "Balance is not sufficient", http.StatusBadRequest)
						return
					}
					opType = 2 // withdrawal
				}

				returnMap := database.DoOperation(opType, accountId, nil, floatAmount) // with balance and uuidv4

				jh.WriteDataToJSON(w, returnMap, http.StatusOK)

			}
		}
	}
}

func ApiAccountAccountIdPut(w http.ResponseWriter, r *http.Request) {
	accountId := chi.URLParam(r, "accountId")
	checkAccount := database.CheckAccountId(accountId, true)
	if len(accountId) == 0 || checkAccount <= 0 {
		if checkAccount == 0 {
			NoResourceFound(w, r)
		} else {
			noCorrectResourceFound(w, r, true)
		}
	} else {
		rMap := jh.ReadJSONToMap(r)
		name := getSingleValue(r, "name", rMap)
		surname := getSingleValue(r, "surname", rMap)

		if len(name) == 0 || len(surname) == 0 {
			missingParameters(w, r)
		} else {
			if !database.UpdateAccountField(accountId, name, "name") || !database.UpdateAccountField(accountId, surname, "surname") {
				failed(w, r)
			} else {
				success(w, r)
			}
		}
	}
}

func ApiAccountAccountIdPatch(w http.ResponseWriter, r *http.Request) {
	accountId := chi.URLParam(r, "accountId")
	checkAccount := database.CheckAccountId(accountId, true)
	if len(accountId) == 0 || checkAccount <= 0 {
		if checkAccount == 0 {
			NoResourceFound(w, r)
		} else {
			noCorrectResourceFound(w, r, true)
		}
	} else {
		rMap := jh.ReadJSONToMap(r)
		name := getSingleValue(r, "name", rMap)
		surname := getSingleValue(r, "surname", rMap)

		if len(name) > 0 && len(surname) > 0 {
			jh.WriteDataToJSON(w, "Both name and surname can't be passed", http.StatusBadRequest)
		} else {
			if len(name) == 0 && len(surname) == 0 {
				missingParameters(w, r)
			} else { // only one now, ok
				var field, newVal string
				if len(surname) != 0 {
					field = "surname"
					newVal = surname
				} else {
					field = "name"
					newVal = name
				}
				if !database.UpdateAccountField(accountId, newVal, field) {
					failed(w, r)
				} else {
					success(w, r)
				}
			}
		}
	}
}

func ApiAccountAccountIdHead(w http.ResponseWriter, r *http.Request) {
	getAccountIdHelper(w, r, true, true)
}

// /api/transfer

func ApiTransferPost(w http.ResponseWriter, r *http.Request) {
	rMap := jh.ReadJSONToMap(r)
	from := getSingleValue(r, "from", rMap)
	to := getSingleValue(r, "to", rMap)
	amount := getSingleValue(r, "amount", rMap)

	if len(amount) == 0 || len(from) == 0 || len(to) == 0 {
		missingParameters(w, r)
	} else {
		checkAccountFrom := database.CheckAccountId(from, true)
		checkAccountTo := database.CheckAccountId(to, true)
		if checkAccountFrom <= 0 || checkAccountTo <= 0 {
			jh.WriteDataToJSON(w, "One or more id is invalid, or inactive", http.StatusBadRequest)
			return
		}

		floatAmount, err := strconv.ParseFloat(amount, 64)
		if err != nil {
			jh.WriteDataToJSON(w, "Failed to parse amount", http.StatusInternalServerError)
		} else {
			if floatAmount < 0 {
				jh.WriteDataToJSON(w, "Amount can't be negative", http.StatusBadRequest)
				return
			}

			if !database.HasEnoughMoney(from, floatAmount) {
				jh.WriteDataToJSON(w, "Balance is not sufficient", http.StatusBadRequest)
				return
			}

			returnMap := database.DoOperation(0, from, &to, floatAmount) // with new balances and uuidv4
			jh.WriteDataToJSON(w, returnMap, http.StatusOK)
		}
	}
}

// /api/divert

func ApiDivertPost(w http.ResponseWriter, r *http.Request) {
	rMap := jh.ReadJSONToMap(r)
	id := getSingleValue(r, "id", rMap)

	if len(id) == 0 {
		missingParameters(w, r)
	} else {
		if !isValidUUID(id) {
			jh.WriteDataToJSON(w, "Invalid UUID v4", http.StatusBadRequest)
			return
		}

		if !database.CheckOperationId(id) {
			jh.WriteDataToJSON(w, "Invalid operation id", http.StatusBadRequest)
			return
		}

		oldOpData := database.GetOperationData(id)

		opType := oldOpData["opType"].(int)
		if opType == 4 { // already cancelled
			jh.WriteDataToJSON(w, "Can't divert an already cancelled operation", http.StatusBadRequest)
		} else if opType == 3 { // cancellation
			jh.WriteDataToJSON(w, "Can't divert a cancellation", http.StatusBadRequest)
		} else if opType != 0 { // deposit or withdrawal
			jh.WriteDataToJSON(w, "Can't divert a deposit or withdrawal", http.StatusBadRequest)
		} else { // transfer

			returnMap, err := database.DivertOperation(id, oldOpData)
			if err != nil {
				jh.WriteDataToJSON(w, err.Error(), http.StatusBadRequest)
				return
			}

			jh.WriteDataToJSON(w, returnMap, http.StatusOK)
		}
	}
}

// NEW ENDPOINTS HERE

// /api/inactive

func ApiInactiveGet(w http.ResponseWriter, r *http.Request) {
	jh.WriteDataToJSON(w, database.GetAllAccounts(false), http.StatusOK)
}

func ApiInactiveDelete(w http.ResponseWriter, r *http.Request) {
	deleteAccountHelper(w, r, false)
}

// /api/inactive/{accountId}

func ApiInactiveAccountIdGet(w http.ResponseWriter, r *http.Request) {
	getAccountIdHelper(w, r, false, false)
}

func ApiInactiveAccountIdHead(w http.ResponseWriter, r *http.Request) {
	getAccountIdHelper(w, r, true, false)
}
