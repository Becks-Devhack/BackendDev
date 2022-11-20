package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"time"
)

type full_data struct {
	Array []string
}

func get_last_30days_data() string {
	pastTime := time.Now().AddDate(0, 0, -30)

	c := http.Client{}
	p_year := pastTime.Year()
	p_month := pastTime.Month()
	p_day := pastTime.Day()
	year := time.Now().Year()
	month := time.Now().Month()
	day := time.Now().Day()

	zero_thing := ""
	if day < 10 {
		zero_thing = "0"
	}

	p_zero_thing := ""
	if p_day < 10 {
		zero_thing = "0"
	}
	p_date := strconv.Itoa(p_year) + "-" + strconv.Itoa(int(p_month)) + "-" + p_zero_thing + strconv.Itoa(p_day)
	date := strconv.Itoa(year) + "-" + strconv.Itoa(int(month)) + "-" + zero_thing + strconv.Itoa(day)
	resp, err := c.Get(fmt.Sprintf("http://fitbit:80/watch/%s/%s", p_date, date))
	if err != nil {
		return fmt.Sprint("Error %s", err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return fmt.Sprintf("Error %s", err)
	}
	return string(body)
}

func get_requests(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		switch r.URL.Path {
		case "/watch":
			data, _ := ioutil.ReadFile("data.txt")
			w.Write([]byte(data))
			break
		case "/stress_levels":
			c := http.Client{}
			data, _ := ioutil.ReadFile("data.txt")
			req, _ := http.NewRequest("GET", "http://ai:80/data", bytes.NewBuffer(data))
			req.Header.Set("Content-Type", "application/json")
			resp, _ := c.Do(req)
			if resp.Status == "200 OK" {
				body, _ := ioutil.ReadAll(resp.Body)
				w.Write([]byte(body))
			}
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
	f, _ := os.Create("data.txt")
	f.WriteString(get_last_30days_data())

	print("Server is ready\n")
	http.HandleFunc("/", get_requests)
	http.ListenAndServe(":8000", nil)
}
