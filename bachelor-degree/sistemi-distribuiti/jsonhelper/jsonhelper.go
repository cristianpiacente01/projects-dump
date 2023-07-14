// cpbank - Pagliaroli Chiara 866160 - Piacente Cristian 866020
// Università degli Studi di Milano - Bicocca
// Progetto di Sistemi Distribuiti, A.A 2021-22, Corso di Laurea in Informatica

package jsonhelper

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"reflect"
	"strings"
)

func DataToMap(v any) map[string]any {
	ret := make(map[string]any)
	ret["content"] = v
	return ret
}

func WriteDataToJSON(w http.ResponseWriter, v any, status int) {
	typeStr := reflect.TypeOf(v).String()
	if !strings.HasPrefix(typeStr, "[") && !strings.HasPrefix(typeStr, "map") { // primitive
		v = DataToMap(v)
	}

	w.Header().Set("Content-Type", "application/json")

	data, err := json.MarshalIndent(v, "", "\t")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		errMsg := "json.MarshalIndent failed: " + err.Error()
		errOut := DataToMap(errMsg)
		data, _ = json.MarshalIndent(errOut, "", "\t")
	} else {
		w.WriteHeader(status)
	}
	w.Write(data)
}

func ReadJSONToMap(r *http.Request) map[string]any {
	if r.Header.Get("Content-Type") != "application/json" {
		return nil // avoid reading the body so I don't lose it
	}
	bytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return nil
	}
	var ret map[string]any
	err = json.Unmarshal(bytes, &ret)
	if err != nil {
		return nil
	}
	return ret
}
