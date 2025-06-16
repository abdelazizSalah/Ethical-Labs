<?php
    /*
        the problems were at these lines: 
            - echo "page <b>$q</b>.php has <i>$row[0]</i> views";
            - echo " this php page <b> " . ($_GET['q']) . " </b> does not exist!";
        The user input is directly echoed without escaping, which can lead to XSS vulnerabilities.
        so we use htmlspecialchars() to escape the user input before echoing it.
        The htmlspecialchars() function converts special characters to HTML entities,
        preventing the execution of any malicious scripts that might be injected by the user.
        This is a common security practice to prevent XSS (Cross-Site Scripting) attacks.


        The code below fixes the issue by escaping the user input before echoing it.
    */


    echo '<i> lookup page views';
    $form = '<form><input type="text" name="q" id="q"></p><p><input type="Submit" value="search"></p></form>';
    echo $form;

    $q = "";
    if (isset($_GET['q'])) {
        $q = $_GET['q'];
    }

    $con = new SQLite3("app.db");
    $query = "SELECT views FROM 'pages' WHERE php='$q'";
    $result = $con->query($query);
    $row = $result->fetchArray();

    // FIX: Escape user input before echoing
    $escaped_q = htmlspecialchars($q, ENT_QUOTES, 'UTF-8');

    if ($row) {
        echo "page <b>$escaped_q</b>.php has <i>$row[0]</i> views";
    } else {
        if (isset($_GET['q'])) {
            echo " this php page <b>$escaped_q</b> does not exist!";
        }
    }
?>
