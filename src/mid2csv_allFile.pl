#!/usr/bin/perl

$srcPath = "~/bishe/midiFile/";
$desPath = "~/bishe/csvFile/";

my @files = glob( $srcPath.'*.mid' );

foreach (@files ){
	# get fileID
	$fileID = substr($_,-9,5); # 00001.mid -> 00001
	$desFile = $desPath.$fileID.'.csv';

	# convert midi into csv using midicsv
	$exec = "midicsv ".$_." ".$desFile;
	system($exec);
}
