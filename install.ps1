If ((Test-Path "$Env:AppData\notflix.py") -eq $False) {
  mkdir $Env:AppData\patchjar
}

cp main.py $Env:AppData\patchjar\patchjar.py

$is = $False
foreach ($_path in ($Env:PATH).split(";")) {
  If ("$_path" -match "patchjar") {
    $is = $True
  }
}

If ($is -eq $False) {
  $oldpath = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).path
  $newpath = "$oldpath;$Env:AppData\patchjar"
  Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH -Value $newpath
}