// cpbank - Pagliaroli Chiara 866160 - Piacente Cristian 866020
// Università degli Studi di Milano - Bicocca
// Progetto di Sistemi Distribuiti, A.A 2021-22, Corso di Laurea in Informatica

package main

import (
	"cpbank/database"
	"cpbank/handlers"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

func main() {
	handlers.OnExitHandler()

	database.Connect()

	r := chi.NewRouter()
	r.Use(middleware.Logger)

	cors := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "DELETE", "PUT", "PATCH", "HEAD"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token", "X-Sistema-Bancario"},
		AllowCredentials: true,
		MaxAge:           300,
	})
	r.Use(cors.Handler)

	fs := http.FileServer(http.Dir("./static"))

	r.Handle("/*", http.StripPrefix("/", fs))

	r.HandleFunc("/transfer", func(res http.ResponseWriter, req *http.Request) {
		http.ServeFile(res, req, "./static/transfer.html")
	})

	r.HandleFunc("/divert", func(res http.ResponseWriter, req *http.Request) {
		http.ServeFile(res, req, "./static/divert.html")
	})

	r.HandleFunc("/accounts", func(res http.ResponseWriter, req *http.Request) {
		http.ServeFile(res, req, "./static/accounts.html")
	})

	r.HandleFunc("/info", func(res http.ResponseWriter, req *http.Request) {
		http.ServeFile(res, req, "./static/info.html")
	})

	r.Route("/api/account", func(r chi.Router) {
		r.Get("/", handlers.ApiAccountGet)
		r.Post("/", handlers.ApiAccountPost)
		r.Delete("/", handlers.ApiAccountDelete)

		r.Route("/{accountId}", func(r chi.Router) {
			r.Get("/", handlers.ApiAccountAccountIdGet)
			r.Post("/", handlers.ApiAccountAccountIdPost)
			r.Put("/", handlers.ApiAccountAccountIdPut)
			r.Patch("/", handlers.ApiAccountAccountIdPatch)
			r.Head("/", handlers.ApiAccountAccountIdHead)
		})
	})

	r.Route("/api/transfer", func(r chi.Router) {
		r.Post("/", handlers.ApiTransferPost)
	})

	r.Route("/api/divert", func(r chi.Router) {
		r.Post("/", handlers.ApiDivertPost)
	})

	r.Route("/api/inactive", func(r chi.Router) {
		r.Get("/", handlers.ApiInactiveGet)
		r.Delete("/", handlers.ApiInactiveDelete)

		r.Route("/{accountId}", func(r chi.Router) {
			r.Get("/", handlers.ApiInactiveAccountIdGet)
			r.Head("/", handlers.ApiInactiveAccountIdHead)
		})
	})

	port := os.Getenv("PORT")
	if len(port) == 0 {
		port = "8080"
	}
	http.ListenAndServe(":"+port, r)
}
