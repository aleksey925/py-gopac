package main

import (
	"bitbucket.org/alex925/gopacparser"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	neturl "net/url"
	"os"
)

var pacPath = flag.String("pacPath", "", "Path to pac file (path or URL)")
var url = flag.String("url", "", "URL of the requested site")

type Result struct {
	Proxy map[string]string
	Error string
}

func buildJson(proxy map[string]*neturl.URL, error error) string {
	errRes := ""
	if error != nil {
		errRes = error.Error()
	}

	result := &Result{}
	result.Error = errRes
	if len(proxy) != 0 {
		result.Proxy = map[string]string{
			"http": proxy["http"].String(),
			"https": proxy["https"].String(),
		}
	} else {
		result.Proxy = map[string]string{}
	}


	resultJson, err := json.Marshal(result)
	if err != nil {
		return "marshal error"
	}
	return string(resultJson)
}

func pathExists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return true, err
}

func checkArgs()  {
	_, errParsingURI := neturl.ParseRequestURI(*pacPath)
	exists, errPathExists := pathExists(*pacPath)
	if errParsingURI != nil && (exists == false || errPathExists != nil) {
			fmt.Println(buildJson(map[string]*neturl.URL{}, errors.New("value packPath is not valid")))
			os.Exit(0)
	}

	_, err := neturl.ParseRequestURI(*url)
	if err != nil {
		fmt.Println(buildJson(map[string]*neturl.URL{}, errors.New("value url is not valid")))
		os.Exit(0)
	}
}

func init() {
	flag.Parse()

	if *pacPath == "" || *url == "" {
		flag.PrintDefaults()
		os.Exit(1)
	}

	checkArgs()
}

func main() {
	result, err := gopacparser.FindProxy(*pacPath, *url)
	fmt.Println(buildJson(result, err))
}
