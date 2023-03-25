<!DOCTYPE html>
<html lang="en">
<link rel="stylesheet" href = "styles.css">
<link rel="stylesheet" href = "normalize.css">
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Toms River Climate Information 1978-2023</title>

<head>
    <div class = "topbox">Toms River Climate Information 1978-2023</div>    
    
</head>
<body>
    <div class = "tabler_index">
        <h3>Most recent month: January 2023</h3>
        <table>
            <tr><td><a href = "http://trclimate.org/Jan2023_temps.png"><img src="Jan2023_temps.png" width=90% height=15%></a></td><td><a href = "http://trclimate.org/Januarytemps_2023.png"><img src="Januarytemps_2023.png" width=50% height=7%></a></td></tr>
            <tr><td><a href = "http://trclimate.org/Jan2023_rainfall.png"><img src="Jan2023_rainfall.png" width=90% height=15%></a></td><td><a href = "http://trclimate.org/Januaryrainfall_2023.png"><img src="Januaryrainfall_2023.png" width=50% height=7%></a></td></tr>
        </table>
        <a href = "http://trclimate.org/Dec2022_ALT.html">December 2022</a>
    </div>    
    <div class="thisyear">
        <h2>2023</h2><br>
        <a href = "http://trclimate.org/Jan2023_ALT.html">Jan</a><br>
        
    </div>
    <div class="calendar">Pick a month and year to access the data for that month
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

</body> 
</html> 

<?php

ob_start();

$first_part = $_POST['month'] . $_POST['year'];
$second_part = "_ALT.html";
$full_url = $first_part.$second_part;

$partial_path = "/var/www/html/trclimate/output.txt";

// Put it all together to use as a filename
$final_name = $first_part.$second_part;
$file_name = fopen($partial_path, "w") or die("Unable to open file!");
fwrite($file_name, $final_name);
fclose($file_name);

include("/var/www/html/trclimate/read_in.php");

ob_end_flush();

exit;
?>