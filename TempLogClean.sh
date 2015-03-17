mv TempLogBad.dat tlb.dat
grep  "Bad" tlb.dat >> TempLogBad.dat

mv TempLog.dat tlu.dat
grep  "Ute" tlu.dat >> TempLog.dat
