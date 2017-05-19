#!/usr/bin/perl

$srcPath = "~/bishe/csvFile/";
$desPath = "~/bishe/noteFile/";

my @files = glob( $srcPath.'*.csv' );

for ($i = 0; $i <48; $i = $i + 1){

	$FileName = substr(@files[$i],-9,5).".txt";

	open(FILE,'<',@files[$i]);
	open(WRITE_FILE,'>',($desPath.$FileName));

	# 正则表达式匹配
	while ($read_line=<FILE>){
	    chomp $read_line;
	    if ($read_line =~ s/(\d+,\s*\d+,\s*Note_\w+,\s*(\d+),\s*)(\d+)(,\s*)(\d+)//){ 
	    	if($5!="0"){
	    		$note = $3;
	    		#printf "$note \n", $note;
	    		print WRITE_FILE "$note \n";
	    	}
	    }
	}

	close $WRITE_FILE;
	close FILE;
}