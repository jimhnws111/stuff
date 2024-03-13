<?php
    $month = $_POST['month'];
    $year = $_POST['year'];
    
    if (empty($month)) {
        echo "String is empty";
    }   

    else {
        echo "String not empty";

    }  
    
    /*
    $first_part = $month.$year;
    $second_part = "_ALT.html";
    $pre = "http://trclimate.org/";
    $fullURL = $pre.$first_part.$second_part;
    echo $month; 
    echo $year;
    echo $fullURL;
    /*header("Location: $fullURL");*/

?>

<!--
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="style.css" />
    <title>Toms River Climate Information 1978-2023</title>
</head>

<body>
    <div class="topBox">
        <a href="http://trclimate.org/index5.php">Toms River Climate Information</a>
    </div>

    <div class="tableFirstPage">
        <h1>Most recent month: March 2023</h1>
        <table>
            <tr>
                <td><a href="http://trclimate.org/Mar2023_temps.png"><img src="Mar2023_temps.png" width=90%
                            height=15%></a></td>
                <td><a href="http://trclimate.org/Marchtemps_2023.png"><img src="Marchtemps_2023.png" width=50%
                            height=7%></a></td>
            </tr>
            <tr>
                <td><a href="http://trclimate.org/Mar2023_rainfall.png"><img src="Mar2023_rainfall.png" width=90%
                            height=15%></a></td>
                <td><a href="http://trclimate.org/Marchrainfall_2023.png"><img src="Marchrainfall_2023.png" width=50%
                            height=7%></a></td>
            </tr>
        </table>
        <a href="http://trclimate.org/Feb2023_ALT.html">February 2023</a>
    </div>

    <div class="thisyear">
        <h2>2023</h2><br>
        <a href="http://trclimate.org/Jan2023_ALT.html">Jan</a><br>
        <a href="http://trclimate.org/Feb2023_ALT.html">Feb</a><br>
        <a href="http://trclimate.org/Mar2023_ALT.html">Mar</a><br>

    </div>
    <div class="leftSide">
        <h2></h2><br>
        <a href="http://trclimate.org/about.html">About TR Climate</a><br><br>
        <a href="">Query the Toms River Database</a><br><br>
        <a href="">Local research</a><br><br>

    </div>

    <div class="calendar">Pick a month and year to access the data for that month
        <form action="" method="POST">
            <table cellspacing="1">
                <tr>
                    <td text-align=center font-size=12>
                        <select name="month" value="">Select Month</option>
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
            </td>
            <td text-align=right>
            </td>
            <td text-align=right font-size=12>
                        <select name="year" value="">Select Year</option>
                            <option value='1978'>1978</option>
                            <option value='1979'>1979</option>
                            <option value='1980'>1980</option>
                            <option value='1981'>1981</option>
                            <option value='1982'>1982</option>
                            <option value='1983'>1983</option>
                            <option value='1984'>1984</option>
                            <option value='1985'>1985</option>
                            <option value='1986'>1986</option>
                            <option value='1989'>1989</option>
                            <option value='1990'>1990</option>
                            <option value='1991'>1991</option>
                            <option value='1992'>1992</option>
                            <option value='1993'>1993</option>
                            <option value='1994'>1994</option>
                            <option value='1995'>1995</option>
                            <option value='1996'>1982</option>
                            <option value='1997'>1997</option>
                            <option value='1998'>1998</option>
                            <option value='1999'>1999</option>
                            <option value='2000'>2000</option>
                            <option value='2001'>2001</option>
                            <option value='2002'>2002</option>
                            <option value='2003'>2003</option>
                            <option value='2004'>2004</option>
                            <option value='2005'>2005</option>
                            <option value='2006'>2006</option>
                            <option value='2007'>2007</option>
                            <option value='2008'>2008</option>
                            <option value='2009'>2009</option>
                            <option value='2010'>2010</option>
                            <option value='2011'>2011</option>
                            <option value='2012'>2012</option>
                            <option value='2013'>2013</option>
                            <option value='2014'>2014</option>
                            <option value='2015'>2015</option>
                            <option value='2016'>2016</option>
                            <option value='2017'>2017</option>
                            <option value='2018'>2018</option>
                            <option value='2019'>2019</option>
                            <option value='2020'>2020</option>
                            <option value='2021'>2021</option>
                            <option value='2022'>2022</option>
                            <option value='2023'>2023</option>
                        </select>       
                
                <input type="submit">
            </table>
        </form>
    </div>
  
    
    <script type="text/javascript">
        var x = "<?php echo"$fullURL"?>";
        open(x, "trclimate");
        close;
    </script> 
 

</body>
</html>
-->