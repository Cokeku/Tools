package main

import (
	"os"
	"io"
	"fmt"
	"flag"
	"path"
)

var (
	src string 
	dst string
)

func init() {
	flag.StringVar(&src ,"srcfile" ,"src.txt" ,"add source file")
	flag.StringVar(&dst ,"dstfile" ,"dst.txt" ,"add destation file")
	flag.Parse()
	fmt.Println(src ,dst)
}

func CopyFile(srcname ,dstname string)(written int64 ,err error){
	srcfile,err := os.OpenFile(srcname ,os.O_RDONLY, 0666)
	if err != nil {
		fmt.Printf("源文件打开失败!\n")
		return 
	}
	defer srcfile.Close()
	
	dstfile,err := os.OpenFile(dstname ,os.O_CREATE | os.O_TRUNC | os.O_WRONLY, 0666)
	if err != nil {
		fmt.Printf("目的文件打开失败!\n")
		return 
	}

	defer dstfile.Close()
	return io.Copy(dstfile, srcfile)
}

func main() {
	dstpathname, dstfilename := path.Split(dst)
	if dstfilename == "" {
		_ , srcfilename := path.Split(src)
		dst = dstpathname + srcfilename
	}
	_ ,err := CopyFile(src ,dst)
	if err != nil {
		fmt.Printf("文件拷贝失败：%v \n",err)
		return
	}
	fmt.Printf("文件拷贝完成!\n") 
}
