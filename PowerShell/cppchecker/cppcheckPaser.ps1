# このスクリプトのファイルパスを取得
$scriptPath = [System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

# 静的解析をかけるディレクトリを設定
#$CHECK_DIR = "D:\SVN\commandTest\"

# 静的解析をかけてXML出力する
#cppcheck --enable=all --xml --force $CHECK_DIR 2>&1 result.xml

#Read-Host "続けるにはENTERキーを押して下さい" 

# 静的解析をかけてXML出力する
.\cppcheckOutputXML.bat

# XMLファイル読み込み
$openFile = [System.IO.File]::OpenText("$scriptPath\result.xml")
$resultXML = [xml]$openFile.ReadToEnd()
$openFile.Close()

# 全エラー要素を表示
foreach ($errors in $resultXML.results.error) 
{
    # ファイル名が空白なら表示しない
    if([bool]$errors.file)
    {
        # ファイルが存在するものをXML出力する
        svn blame --xml $errors.file>blame.xml

        $openFile = [System.IO.File]::OpenText("$scriptPath\blame.xml")
        $blameXML = [xml]$openFile.ReadToEnd()
        $openFile.Close()

        #foreach ($blameLine in $blameXML.blame.target.entry) 
        #{
        #     Write-Host "blame Line" $blameLine.'line-number'
        #}
        
        Write-Host "==START="
        Write-Host "file    :" $errors.file
        Write-Host "line    :" $errors.line
        Write-Host "msg     :" $errors.msg
        Write-Host "User    :" $blameXML.blame.target.entry[$errors.line - 1].commit.author
        Write-Host "==END==="
    }
 }
