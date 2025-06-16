

<?php
/*
    The problem is that the user input is directly 
    so we need to use prepared statements to prevent SQL injection.
    prepare statements are a way to execute SQL queries in a safe manner, 
    where the user input is treated as data rather than executable code.
    so the bindValue tells the DB to treat the input as a string not as code.

    The code below fixes the issue by using prepared statements.

*/

ini_set('error_reporting', E_ALL);
session_start();

$con = new SQLite3("app.db");

// FIX: Use prepared statements to prevent SQL injection
$stmt = $con->prepare("SELECT password FROM users WHERE name = :username");
$stmt->bindValue(':username', $_POST["username"], SQLITE3_TEXT);
$result = $stmt->execute();

$success = false;
$username = $_POST["username"];
$password = $_POST["password"];

while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    if ($row['password'] === $password) {
        $success = true;
        break;
    }
}

if ($success) {
    $_SESSION['login'] = true;
    $_SESSION['username'] = $username;
    header('Location: /comments.php');
    exit;
} else {
    echo "<h1>Login failed.</h1>";
}
?>
