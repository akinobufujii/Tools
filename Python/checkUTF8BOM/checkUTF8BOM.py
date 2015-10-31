# coding: UTF-8
import sys
import struct
import binascii
import os
import os.path

#------------------------------------
# UTF8BOM付きチェック関数
#------------------------------------
def isUTF8BOM(filename):
	#print u"call isUTF8BOM"
	#print u"file name is %s" % (filename)

	# ファイルが3バイト以下ならUTF8 BOM付きではない
	filesize = os.path.getsize(filename)

	#print u"file size is %d" % (filesize)

	# 3バイト未満なのでUTF8 BOM付きではないです
	if filesize < 3:
		return False

	# ファイルオープン
	infile = open(filename, 'rb')

	str = "" + binascii.hexlify(infile.read(1))
	str += " " + binascii.hexlify(infile.read(1))
	str += " " + binascii.hexlify(infile.read(1))

	#print str

	# ファイルクローズ
	infile.close()

	if str == "ef bb bf":
		return True
	else:
		return False

#------------------------------------
# 再帰的にファイル、フォルダを取得
#------------------------------------
def findAllFiles(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

#------------------------------------
# 使い方を表示
#------------------------------------
def useThisProgram():
	print u"指定されたディレクトリ以下のファイルが\nUTF8BOM付きかどうかをチェックするツールです\n"
	print u"引数"
	print u"第1引数	チェックするディレクトリ"
	print u"第2引数	チェックするファイル拡張子リストファイル"
	print u"第3引数	チェックを除外するフォルダリストファイル"

#====================================
# エントリーポイント
#====================================
# 引数の数を取得して指定数以下なら使い方を表示して終了
argc = len(sys.argv)
if argc < 4:
	print u"※引数の数が足りません※"
	useThisProgram()
	sys.exit()

# 入力されたディレクトリ以下の全ファイル名を出力
allFilesListName = "allFileList.list"
writeFileObject = open(allFilesListName, 'w')

for file in findAllFiles(sys.argv[1]):
	if os.path.isdir(file) == False:
		writeFileObject.write(file + '\n')

writeFileObject.close()

# 指定された拡張子のみの配列を作成する
extList = []
for ext in open(sys.argv[2], 'r'):
	extList.append('.' + ext.rstrip('\n'))

# 除外ディレクトリの配列を作成する
ignoreList = []
for ignore in open(sys.argv[3], 'r'):
	ignoreList.append(sys.argv[1] + '\\' + ignore.rstrip('\n'))

# 指定された拡張子のみのリストを作成する
checkFileListName = "checkFileList.list"

writeFileObject = open(checkFileListName, 'w')
for files in open(allFilesListName, 'r'):
	# 指定された拡張子ならファイルに記載する
	for checkExt in extList:
		temp, ext = os.path.splitext(files)
		if checkExt == ext.rstrip('\n'):
			# 除外リストに含まれていないか確認する
			writeOK = True
			for ig in ignoreList:
				if files.startswith(ig):
					writeOK = False
					break
			# チェックを突破したなら書き込む
			if writeOK:
				writeFileObject.write(files)
			break

writeFileObject.close()

# チェックファイルリストからUTF8BOM付きかを再帰的にチェック
resultStr = ""
resultCount = 0;

for checkFile in open(checkFileListName, 'r'):
	checkFile = checkFile.rstrip('\n')
	if isUTF8BOM(checkFile) == False:
			if resultCount == 0:
				resultStr += checkFile
			else:
				resultStr += '\n' + checkFile

			resultCount += 1

# すべて表示
print "Total %d" % (resultCount)
print "======Not UTF8BOM====="
print resultStr
print u"======Not UTF8BOM====="
