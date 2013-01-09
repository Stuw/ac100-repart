#!/bin/bash

CROSS_COMPILER=arm-linux-gnueabihf-
EXTERNALS="./externals"

mkdir -p "$EXTERNALS"


# nvflash
nvflash_zip_url="http://stuw.narod.ru/ac100/nvflash-12alpha.zip"
if [[ ! -e "${EXTERNALS}/nvflash" ]]; then
	wget "$nvflash_zip_url" -P "$EXTERNALS"
	unzip ./externals/nvflash-12alpha.zip -d "$EXTERNALS"
fi



function git_repo() {
	local dir="$1"
	local repo="$2"

	if [[ ! -e $dir ]]; then
		git clone $repo $dir
		pushd $dir
	else
		pushd $dir
		git clean -fdx
		git pull
	fi
}


pushd "$EXTERNALS"


# cbootimg / bct_dump
cbootimg_repo="-b master git://gitorious.org/cbootimage/cbootimage.git"
git_repo "cbootimage" "$cbootimg_repo"
make
popd


# uboot
#uboot_repo="-b next git://git.denx.de/u-boot-tegra.git"
#git_repo "u-boot-tegra" "$uboot_repo"
#make paz00_config CROSS_COMPILE=$CROSS_COMPILER
#make CROSS_COMPILE=$CROSS_COMPILER
#popd


# EXTERNALS
popd
