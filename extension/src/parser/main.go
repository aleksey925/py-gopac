package main

// #include <stdlib.h>
import "C"

import (
	"github.com/aleksey925/gopacparser"
	"encoding/json"
	neturl "net/url"
	"unsafe"
)


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
			"http":  proxy["http"].String(),
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

//export ParseFile
func ParseFile(path string, url string) *C.char {
    proxies, err := gopacparser.FindProxy(path, url)
    result := buildJson(proxies, err)
	return C.CString(result)
}

//export FreePointer
func FreePointer(pointer *C.char) {
    C.free(unsafe.Pointer(pointer))
}

func main() {}
