<?php
obs_start();

$file = file_get_contents('/var/www/html/trclimate/output.txt', true);
$pre = 'http://trclimate.org/';
$full_url = $pre.$file;
echo $full_url;
header("Location: $full_url");

obs_end_flush();