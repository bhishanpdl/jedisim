#!bash
#
###########################################################
# Author: Bhishan Poudel
# Date  : May 7, 2018
# Topic : Upload jedisim outputs
###########################################################
#
#  1. First create a repo jout_z0.7_000_099 in github.
#
#  2. Clone the repo to ~/Rsh_out/jout_z0.7_000_099
#
#  3. Copy the folder from jedisim outputs and rename it as:
#         ~/Rsh_out/orig_jout_z0.7_000_099
#
#  4. Upload some files from orig_out to jout multiple times.
#
#     jout = "orig_jout_z0.7_000_099"
#     repo = "jout_z0.7_000_099"
#
#  NOTE: While we are uploading from local, DO NOT CHANGE in remote.
#  NOTE: Do not run multiple instances of upload_to_github.sh it will hang.
# 
jout=$1 # e.g. orig_jout_z0.7_000_099  without / sign.
repo=${jout:5}

# Zip the folder for backup
function zip_the_repo() { zip -r orig_$repo.zip orig_$repo; }


# First activate bpJedisim github account
function activate_bpJedisim () {
    ssh-add ~/.ssh/id_rsa_bpJedisim
    git config --global user.user bpJedisim
    git config --global user.email bhishanpdl3@gmail.com
}


function upload_text_files () {
    mv orig_$repo/catalog $repo/catalog
    mv orig_$repo/catalog90 $repo/catalog90
    mv orig_$repo/dislist $repo/dislist
    mv orig_$repo/dislist90 $repo/dislist90

    # Now cd to catalog and upload files
    cd $repo/catalog
    git add *.txt
    git commit -m "Added text files"
    git push
    cd -
}


# usage: upload_34_fitsfiles lsst
function upload_34_fitsfiles () {
    local OUTPUT=$repo/$1
    mkdir $OUTPUT

    for file in $(ls orig_$OUTPUT | grep -v / | sort | tail -34)
    do
        ifile="orig_$OUTPUT/$file"
        ofile="$OUTPUT/$file"
        # echo $ofile
        mv $ifile $ofile
    done


    # Upload 34 files
    cd $OUTPUT
    git add --all
    git commit -m "Uploaded jedisim outputs"
    git push
    cd -
}

#=====================================================

# NOTE: Rename the input folder at the top of this script.

# zip_the_repo
# activate_bpJedisim

# upload txt files
upload_text_files &&

# upload lsst files 34 at a time
upload_34_fitsfiles lsst &&
upload_34_fitsfiles lsst &&
upload_34_fitsfiles lsst &&

# upload lsst90 files 34 at a time
upload_34_fitsfiles lsst90 &&
upload_34_fitsfiles lsst90 &&
upload_34_fitsfiles lsst90 &&

# upload lsst files 34 at a time
upload_34_fitsfiles lsst_mono &&
upload_34_fitsfiles lsst_mono &&
upload_34_fitsfiles lsst_mono &&

# upload lsst90 files 34 at a time
upload_34_fitsfiles lsst_mono90 &&
upload_34_fitsfiles lsst_mono90 &&
upload_34_fitsfiles lsst_mono90 &&

echo "All files uploaded!"

# Command: 1. First clone the repo jout_z0.7_000_099
#          2. Make sure there is dir orig_jout_z0.7_000_099
#
# Command: bash upload_to_github.sh orig_jout_z0.7_000_099 # no / sign
