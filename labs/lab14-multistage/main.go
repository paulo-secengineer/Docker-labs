package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	startTime := time.Now()

	fmt.Printf(" App Iniciado em: %s\n", startTime.Format("15:04:05"))
	fmt.Printf(" Arquitetura: %s/%s\n", runtime.GOOS, runtime.GOARCH)
	fmt.Printf(" Versão do Go: %s\n", runtime.Version())
	fmt.Printf(" CPUs detectadas: %d\n", runtime.NumCPU())

	fmt.Println("\nMonitorando recursos (Ctrl+C para sair)...")
	
	for {
		var m runtime.MemStats
		runtime.ReadMemStats(&m)
		
		uptime := time.Since(startTime).Round(time.Second)
		
		fmt.Printf("\r  Uptime: %s |  Memória em uso: %v KB  ", uptime, m.Alloc/1024)
		
		time.Sleep(2 * time.Second)
	}
}
