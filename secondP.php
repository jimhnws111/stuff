<!DOCTYPE html>
<html>

<form method=post name=f1 action=''><input type=hidden name=todo value=submit>
        <table cellspacing="0" >
        <tr><td text-align=center  >   
        <select name=month value=''>Select Month</option>
        <option value='Jan'>January</option>
        <option value='Feb'>February</option>
        <option value='Mar'>March</option>
        <option value='Apr'>April</option>
        <option value='May'>May</option>
        <option value='Jun'>June</option>
        <option value='Jul'>July</option>
        <option value='Aug'>August</option>
        <option value='Sep'>September</option>
        <option value='Oct'>October</option>
        <option value='Nov'>November</option>
        <option value='Dec'>December</option>
        </select>
        </td><td text-align=right >   
        </td><td text-align=right font-size=7>Year(yyyy)
        <input type=text name=year size=10 value=2022>
        <input type=submit value=Submit>
        </table>
</form>

<?php
$year = $_POST['year'];
$month = $_POST['month'];

$first_part = $month.$year;
$second_part = "_ALT.html";

$partial_path = "/Users/jameshayes/output.txt";

// Put it all together to use as a filename
$final_name = $first_part.$second_part;
$file_name = fopen($partial_path, "w") or die("Unable to open file!");
fwrite($file_name, $final_name);
fclose($file_name);

$file_open = fopen($partial_path, "r") or die("Unable to open file!");
$last_piece = fgets($file_open);
fclose($file_open);

$file_open = fopen($partial_path, "r") or die("Unable to open file!");
$last_piece = fgets($file_open);
fclose($file_open);

$file_open = fopen($partial_path, "r") or die("Unable to open file!");
$last_piece = fgets($file_open);
fclose($file_open);
$first_piece = "http://trclimate.org/";
$full_url = $first_piece.$last_piece;

$curl = curl_init($full_url);
curl_setopt($curl, CURLOPT_URL, $full_url);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($curl);
curl_close($curl);
print $response;

#header("Location: " . $full_url);
#die();
?>