package main

import (
	"net/http"
)

func sendURL(w http.ResponseWriter, r *http.Request) {
	var link1 = "dummy1"
	var link2 = "dummy2"
	var link3 = "dummy3"

	if r.Method == "GET" {
		switch r.URL.Path {
		case "/APK1":
			w.Write([]byte(link1 + "\n"))
			break
		case "/APK2":
			w.Write([]byte(link2 + "\n"))
			break
		case "/APK3":
			w.Write([]byte(link3 + "\n"))
			break
		default:
			http.NotFound(w, r)
		}
	} else {
		w.WriteHeader(http.StatusNotImplemented)
		w.Write([]byte(http.StatusText(http.StatusNotImplemented) + " \n"))
	}
}

func main() {
	http.HandleFunc("/", sendURL)
	http.ListenAndServe(":8000", nil)
}
