<!DOCTYPE html>
<html lang="en">
<link rel="stylesheet" href = "styles.css">
<link rel="stylesheet" href = "normalize.css">
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<head>
<body>
 <?php

$f = fopen("/Users/jameshayes/Sites/HiLoRain.txt", "r");

$data = fgetcsv($f, 1000, ",");

while (($data = fgetcsv($Open, 1000, ",")) !== FALSE) 
{
  
    $array[] = $data;
}

fclose($f);

echo"FUCK";

echo "<pre>";
  //To display array data
  var_dump($array);
  echo "</pre>";

?>


</body>
</head>
</html>