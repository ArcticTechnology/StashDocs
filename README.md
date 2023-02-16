# Stash Docs
This is a sandbox package that is currently under construction.
* Github repo: https://github.com/ArcticTechnology/StashDocs

## Documentation
Stash Docs allows you to obfuscate files through the stash feature. Stash allows you to map files to alias names and a pre-defined location. Then the Scrambler will alter the name and move it to the pre-defined location, and then scramble the metadata of the files and directories to hide the file. At any time, Scrambler can retrieve the stashed files by providing a password. In order to use stash you have to setup a config file that tells the Scrambler where to send your stashed files to and what their new names will be.

Instructions on creating a config file:
1. Create your .config based off of config-example.txt file in this repository [https://github.com/ArcticTechnology/StashDocs/tree/main/config]. The .config file follows JSON formatting and should contain these pieces of data:
```
{"origin_dir": "/home/origin_directory/",
"stash_dir": "/home/stash_directory/",
"stash_key": {
"filename1": "stashed_filename1",
"filename2": "stashed_filename2",
"filename3": "stashed_filename3"}}
```
* ```"origin_dir": "/home/origin_directory/"``` - This is the directory where the files you want to stash are located.
* ```"stash_dir": "/home/stash_directory/"``` - This is the directory where you want to stash your files.
* ```"filename1": "stashed_filename1"``` - This is the mapping of the original file name and the name you want the new file name you want the file to be changed to.

2. Save your file as .config and place it into your scrambler app's config folder. Here is an example of what the directory looks like:
```
C:/Users/username/AppData/Local/Python3/StashDocs/config
```
3. Highly recommended: Password encrypt this .config file with the Scrambler app. This will create .config-c which is still recognizable by Scrambler.
4. Highly recommended: Once you have the encrypted version (.config-c) you can delete the original .config file as it is no longer needed. You defeat the purpose of an encrypted config file if the unencrypted version is still lying around. Note if stash detects an unencrypted version, you can choose to have stash encrypt it for you which will automatically delete the original.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/main/btcaddr1.png?raw=true)
