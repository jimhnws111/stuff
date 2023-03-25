<?php
$file_open = fopen("/Users/jameshayes/output.txt", "r") or die("Unable to open file!");
$last_piece = fgets($file_open);
fclose($file_open);

header("Location: http://trclimate.org/" .$last_piece);