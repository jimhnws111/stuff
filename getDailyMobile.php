<?php
session_start();
?>

<?php
$servername = "3.135.162.69";
$username = "chuckwx";
$password = "jfr716!!00";
$dbname = "trweather";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Function to sanitize input
function sanitizeInput($input)
{
    return htmlspecialchars(trim($input));
}

?>

<html>
<head>
    <meta charset="utf-8" />  
    <meta name="viewport" content="width=device-width, initial-scale=1" />  
    <link rel="stylesheet" media="screen and (min-width: 900px)" href="stylesQuery.css" />
    <link rel="stylesheet" media="screen and (max-width: 600px) " href="stylesDailyMobile.css" />
    <link rel="stylesheet" href="normalize.css">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Get Daily Data from the Database</title>
</head>
<body>
    <a href="http://trclimate.org">
    <div class="topBox">Daily Data</div>
    </a>
    <div class="query_boxMonth">


    <form method='post' action='getDailyMobile.php'>

        <label>Year </label>
        <select name='Year' id='Year' onchange='this.form.submit();'>
            <option value=''>Select a Year</option>
            <?php
            $sql = "SELECT DISTINCT Year FROM trw";
            $result = $conn->query($sql);
            while ($row = $result->fetch_assoc()) {
                echo "<option value='" . sanitizeInput($row['Year']) . "'>" . sanitizeInput($row['Year']) . "</option>";
        }
        ?>
        </select>

    </form>
    </div>
    </div>

<?php


// Check if the form is submitted
if (isset($_POST['Year'])) {
    $year = sanitizeInput($_POST['Year']);
    $_SESSION['Year'] = $_POST['Year'];
              
}
   

    // Get Month from Year using prepared statement
    $stmt = $conn->prepare("SELECT DISTINCT Month FROM trw WHERE Year = ?");
    $stmt->bind_param("s", $year);
    $stmt->execute();
    $result = $stmt->get_result();

    ?>
    
    <div class="query_boxMonth">

    <form method='post' action='getDailyMobile.php'>
        <label>Month </label>
        <select name='Month' id='Month' onchange='this.form.submit();'>
            <option value=''>Select a Month</option>
            <?php
            while ($row = $result->fetch_assoc()) {
                echo "<option value='" . sanitizeInput($row['Month']) . "'>" . sanitizeInput($row['Month']) . "</option>";
            }
            ?>
        </select>
    </form>
    </div>
        
    <?php
    $stmt->close();
    ?>

<?php
// Check if the form is submitted
if (isset($_POST['Month'])) {
    $month = sanitizeInput($_POST['Month']);
    $_SESSION['Month'] = $_POST['Month'];
    $month1 = $_SESSION['Month'];
    $year1 = $_SESSION['Year'];

}    
    
    // Get Day from Month using prepared statement
    $stmt = $conn->prepare("SELECT DISTINCT Day FROM trw WHERE Year = '$year1' AND Month = ?");
    $stmt->bind_param("s", $month);
    $stmt->execute();
    $result = $stmt->get_result();
    
    ?>

    <div class="query_boxMonth">

    <form method='post' action='getDailyMobile.php'>
        <label>Day </label>
        <select name='Day' id='Day' onchange='this.form.submit();'>
            <option value=''>Select a Day</option>
            <?php
            while ($row = $result->fetch_assoc()) {
                echo "<option value='" . sanitizeInput($row['Day']) . "'>" . sanitizeInput($row['Day']) . "</option>";
            }
            ?>
        </select>
    </form>
    </div>
    
<?php
$stmt->close();

// Check if the form is submitted
if (isset($_POST['Day'])) {
    $day = sanitizeInput($_POST['Day']);
    $_SESSION['Day'] = $_POST['Day'];
    $day1 = $_SESSION['Day'];
    $month1 = $_SESSION['Month'];
    $year1 = $_SESSION['Year'];
                      
}

?>

<?php

// Put the data together for one last sql statement


$sqlFinal = "SELECT * from trw WHERE Year = '$year1' AND Month = '$month1' AND Day = '$day1'";
$result = $conn->query($sqlFinal);
$chuck = $result->fetch_all(MYSQLI_ASSOC);
$chuckwx = json_encode($chuck);
//echo '<prev>'; print_r($chuckwx); echo '</prev>';

$file = fopen("/var/www/html/000/daily.txt", "w") or die("Unable to open file");

fwrite($file, $chuckwx);
fclose($file);

$conn->close();

$output = shell_exec('/var/www/html/000/dailyProcess.sh 2>&1');
//var_dump($output);
//header("Location: http://3.135.162.69/dailyTest.html");


?>

<div id="display1" style="position: absolute;top: 30%;left: 0;"></div>
<script>
  function load_anotherpage() {
    document.getElementById("display1").innerHTML =
      '<embed type="text/html" src="http://3.135.162.69/dailyTest1.html" width="430" height="450">';
  }

  load_anotherpage();
</script>
</div>

</body>
</html>