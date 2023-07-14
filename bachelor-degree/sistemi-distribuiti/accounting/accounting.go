// cpbank - Pagliaroli Chiara 866160 - Piacente Cristian 866020
// Università degli Studi di Milano - Bicocca
// Progetto di Sistemi Distribuiti, A.A 2021-22, Corso di Laurea in Informatica

package accounting

import (
	"cpbank/database"

	"crypto/rand"
	"encoding/hex"
)

func generateId() string {
	var ret string
	var bytes []byte
	var check bool

	for {
		bytes = make([]byte, 10)
		rand.Read(bytes)
		ret = hex.EncodeToString(bytes)
		check = database.CheckAccountId(ret, true) != 0
		if !check {
			break
		}
	}

	return ret
}

func NewAccount(name string, surname string) string {
	accountId := generateId()
	database.AddAccount(accountId, name, surname)
	return accountId
}
