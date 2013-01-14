#!/bin/bash

log_file="${1:-./generated/init-externals.log}"
log_file=$(readlink -f "${log_file}")

CROSS_COMPILER=arm-linux-gnueabihf-
EXTERNALS="./externals"

mkdir -p "$EXTERNALS"

RES=0

function set_error() {
	RES=1
}

# nvflash
nvflash_zip_url="http://stuw.narod.ru/ac100/nvflash-12alpha.zip"
#if [[ ! -e "${EXTERNALS}/nvflash" ]]; then
	echo "Downloading nvflash..."
	wget "$nvflash_zip_url" -P "$EXTERNALS" > "${log_file}" 2>&1 || set_error
	echo "Unpacking nvflash..."
	unzip -u ./externals/nvflash-12alpha.zip -d "$EXTERNALS" > ${log_file} 2>&1 || set_error
	chmod a+x "${EXTERNALS}/nvflash/nvflash" || set_error
	chmod a+x "${EXTERNALS}/nvflash/mkbootimg" || set_error
	echo "Done."
#fi

# uboot sos image
if [[ ! -e "${EXTERNALS}/uboot-sos.img" ]]; then
	echo "Downloading uboot sos image..."
	wget http://ac100.wikispaces.com/file/view/\
uboot-sos.img/398037302/uboot-sos.img -P "$EXTERNALS" > "${log_file}" 2>&1 || set_error
	echo "Done."
fi


# gpt-surgeon.py
gpt_surgeon_url="http://bat-country.us/code/GPTools/trunk/gpt_surgeon.py?revision=130&view=co"
gpt_surgeon="${EXTERNALS}/gpt_surgeon.py"
if [[ ! -e "${gpt_surgeon}" ]]; then
	echo "Downloading gpt-surgeon..."
	wget "${gpt_surgeon_url}" -O "${gpt_surgeon}" > "${log_file}" 2>&1 || set_error
	chmod a+x "${gpt_surgeon}" || set_error
	echo "Done."
fi


function git_repo() {
	local dir="$1"
	local repo="$2"

	if [[ ! -e $dir ]]; then
		echo "Cloning $dir..."
		git clone $repo $dir > "${log_file}" 2>&1 || set_error
		pushd $dir > "${log_file}" 2>&1 || set_error
	else
		echo "Updating $dir..."
		pushd $dir > "${log_file}" 2>&1 || set_error
		git clean -fdx > "${log_file}" 2>&1 || set_error
		git pull > "${log_file}" 2>&1 || set_error
	fi
	echo "Done."
}


pushd "$EXTERNALS" > /dev/null


# cbootimg / bct_dump
cbootimg_repo="-b master git://gitorious.org/cbootimage/cbootimage.git"
git_repo "cbootimage" "$cbootimg_repo"
echo "Compiling cbootimage..."
make > "${log_file}" 2>&1 || set_error
echo "Done."
popd > /dev/null


# uboot
#uboot_repo="-b next git://git.denx.de/u-boot-tegra.git"
#git_repo "u-boot-tegra" "$uboot_repo"
#make paz00_config CROSS_COMPILE=$CROSS_COMPILER
#make CROSS_COMPILE=$CROSS_COMPILER
#popd


# EXTERNALS
popd > /dev/null

exit $RES
