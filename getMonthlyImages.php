<?php

if($_POST['Month'] and $_POST['Year']){
    $month = $_POST['Month'];
    $year = $_POST['Year'];
}            

// render month/year names to attach to images

$monthYear = $month.$year;
$temp_suffix = '_temps.png';
$rain_suffix = '_rainfall.png';
$newTemps = 'Temps.png';
$newRain = 'Rain.png';

$siteID = 'http://trclimate.org/';
$siteID1 = 'http://trclimate.org/images/';

$tempImage = $siteID.$monthYear.$temp_suffix;
$rainImage = $siteID.$monthYear.$rain_suffix;
$newTempImage = $siteID1.$monthYear.$newTemps;
$newRainImage = $siteID1.$monthYear.$newRain;

?>

<!DOCTYPE html>

<head>
    <html lang="en">
    
    <link rel="stylesheet" href="normalize.css">
    
    <link rel="stylesheet" media="screen and (min-width: 900px)" href="valTest.css" />
    <link rel="stylesheet" media="screen and (max-width: 600px) " href="valTestMobile.css" />

    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Monthly Images</title>
</head>

<body>
    
    <p>Get Monthly Images</p>
    <br>
        <div class="testBox1">
        <form action="getMonthlyImages.php" method="post">
        <label>Year</label>
            <select id='Year' name='Year'>
                <option value="1978">1978</option>
                <option value="1979">1979</option>
                <option value="1980">1980</option>
                <option value="1981">1981</option>
                <option value="1982">1982</option>
                <option value="1983">1983</option>
                <option value="1984">1984</option>
                <option value="1985">1985</option>
                <option value="1986">1986</option>
                <option value="1989">1989</option>
                <option value="1990">1990</option>
                <option value="1991">1991</option>
                <option value="1992">1992</option>
                <option value="1993">1993</option>
                <option value="1995">1995</option>
                <option value="1996">1996</option>
                <option value="1997">1997</option>
                <option value="1998">1998</option>
                <option value="1999">1999</option>
                <option value="2000">2000</option>
                <option value="2001">2001</option>
                <option value="2002">2002</option>
                <option value="2003">2003</option>
                <option value="2004">2004</option>
                <option value="2005">2005</option>
                <option value="2006">2006</option>
                <option value="2007">2007</option>
                <option value="2008">2008</option>
                <option value="2009">2009</option>
                <option value="2010">2010</option>
                <option value="2011">2011</option>
                <option value="2012">2012</option>
                <option value="2013">2013</option>
                <option value="2014">2014</option>
                <option value="2015">2015</option>
                <option value="2016">2016</option>
                <option value="2017">2017</option>
                <option value="2018">2018</option>
                <option value="2019">2019</option>
                <option value="2020">2020</option>
                <option value="2021">2021</option>
                <option value="2022">2022</option>
                <option value="2023">2023</option>
                <option value="2024">2024</option>
            </select><br><br>
            <label>Month</label>
            <select id='Month' name='Month'>
                <option value="Jan">Jan</option>
                <option value="Feb">Feb</option>
                <option value="Mar">Mar</option>
                <option value="Apr">Apr</option>
                <option value="May">May</option>
                <option value="Jun">Jun</option>
                <option value="Jul">Jul</option>
                <option value="Aug">Aug</option>
                <option value="Sep">Sep</option>
                <option value="Oct">Oct</option>
                <option value="Nov">Nov</option>
                <option value="Dec">Dec</option>
            </select><br>
            <input type="submit" value="Submit">
                           
         </form>
        </div>

<div class="sizeIt">

<div id="x"></div>
<script>
    
    t = "<?php echo"$tempImage"?>"; 
    r = "<?php echo"$rainImage"?>";  
    nt = "<?php echo"$newTempImage"?>";
    nr = "<?php echo"$newRainImage"?>";

    var img = document.createElement("img");
    img.src = t;
    var src = document.getElementById("x");
    src.appendChild(img);

    var img = document.createElement("img");
    img.src = r;
    var src = document.getElementById("x");
    src.appendChild(img);
  
 </script>  
 </div>

 <div class="sizeIt2">

 <div id="y"></div>  
 <script>

    var img = document.createElement("img");
    img.src = nt;
    var src = document.getElementById("y");
    src.appendChild(img);

    var img = document.createElement("img");
    img.src = nr;
    var src = document.getElementById("y");
    src.appendChild(img);

</script>  
</div>

<div class="rockBottom">
<a href="http://trclimate.org" style="font-size: 3vw;">Return to trclimate.org</a>
</div>

</body>
</html>