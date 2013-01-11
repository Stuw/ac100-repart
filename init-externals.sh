#!/bin/bash

CROSS_COMPILER=arm-linux-gnueabihf-
EXTERNALS="./externals"

mkdir -p "$EXTERNALS"

RES=0

function set_error() {
	RES=1
}

# nvflash
nvflash_zip_url="http://stuw.narod.ru/ac100/nvflash-12alpha.zip"
if [[ ! -e "${EXTERNALS}/nvflash" ]]; then
	wget "$nvflash_zip_url" -P "$EXTERNALS" || set_error
	unzip ./externals/nvflash-12alpha.zip -d "$EXTERNALS" || set_error
	chmod a+x "${EXTERNALS}/nvflash/nvflash" || set_error
	chmod a+x "${EXTERNALS}/nvflash/mkbootimg" || set_error
fi



function git_repo() {
	local dir="$1"
	local repo="$2"

	if [[ ! -e $dir ]]; then
		git clone $repo $dir || set_error
		pushd $dir || set_error
	else
		pushd $dir || set_error
		git clean -fdx || set_error
		git pull || set_error
	fi
}


pushd "$EXTERNALS"


# cbootimg / bct_dump
cbootimg_repo="-b master git://gitorious.org/cbootimage/cbootimage.git"
git_repo "cbootimage" "$cbootimg_repo"
make || set_error
popd


# uboot
#uboot_repo="-b next git://git.denx.de/u-boot-tegra.git"
#git_repo "u-boot-tegra" "$uboot_repo"
#make paz00_config CROSS_COMPILE=$CROSS_COMPILER
#make CROSS_COMPILE=$CROSS_COMPILER
#popd


# EXTERNALS
popd

exit $RES
