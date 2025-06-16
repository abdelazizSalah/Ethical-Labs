<?php 
/*
    same idea as search.
    this is the problem: 
        - $comment = '<p>“' . ($_POST['comment']) . '”<br>...';
    This inserts raw user input ($_POST['comment']) directly into an HTML file (comments.txt) — any script tag will be saved and executed for future visitors.
    the solution is also htmlspecialchars() to escape the user input before inserting it into the HTML file.
*/


// Load jQuery and input validator script
$pageStart = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>';

$pageStart .= '<script type="text/javascript">
    function checkValid(a){
        if( /[^a-zA-Z0-9 ]/.test( (a.value)) ) {
            $("#helpBlock").text("Error, invalid characters detected");
            console.log(false);return false;
        } else {
            console.log(true);return true;
        }
    }</script>';

session_start();

// Authentication check
if (!isset($_SESSION['login'])) {
    echo "<h2>You must be logged in to access the comments</h2>";
    die();
}

// Load and display comments
function read_comments() {
    $comments = file_get_contents('comments.txt');

    if (empty($comments)) {
        echo '<p><i>There are no comments at this time.</i></p>';
    } else {
        echo $comments;
    }
}

// Display comment form
function print_form($val) {
    $sign = hash('sha256', $_SESSION['username']);

    echo '<p><i>Leave a question/comment:</i></p>';
    echo '<span id="helpBlock" class="help-block" style="color:red;"></span>';

    $form = '<form method="post" onsubmit="return checkValid(comment)" action="#"><textarea name="comment" id="comment" style="';

    // Highlight invalid input if needed
    if (($val == 1)||($val == 3)) {
        $form .= 'border: 1px solid #912; ';
    }

    $form .= 'width: 80%; height: 10em;">';

    // Preserve submitted comment if invalid
    if ($val != 0) {
        $form .= htmlspecialchars($_POST['comment'] ?? '', ENT_QUOTES, 'UTF-8');
    }

    $form .= '</textarea><p><i>Your name: </i> <b>';
    $form .= '<input type="hidden" name="token256" id="token256" value="' . $sign . '">';
    $form .= $_SESSION['username'] . '</b>';
    $form .= '</p><p><input type="Submit" value="Post comment"></p>';
    $form .= '<span id="helpBlock" class="help-block" style="color:red;"></span></form>';
    $form .= '<form method="post"><p><input type="submit" value="Log me out" name="logout" ></p></form>';

    echo $form;
}

// Handle comment submission
function process_form() {
    $err = 0;
    $sign = hash('sha256', $_SESSION['username']);

    // Handle logout
    if (isset($_POST["logout"])) {
        session_destroy();
        unset($_SESSION['username']);
        echo("<script>window.location = 'index.php';</script>");
    }

    // Handle comment submission
    if (isset($_POST['comment'])) {
        if (empty($_POST['comment'])) {
            echo 'nothing to post!';
            $err++;
        }

        // CSRF token check
        if ($_POST['token256'] != $sign) {
            $err += 4;
            echo 'token does not match';
        }

        if ($err == 0) {
            // FIX: Sanitize comment input to prevent stored XSS
            $safe_comment = htmlspecialchars($_POST['comment'], ENT_QUOTES, 'UTF-8');

            $comment = '<p>“' . $safe_comment . '”<br><span style="text-align: right; font-size: 0.75em;">—' 
                     . $_SESSION['username'] . ', ' . date('F j\, g\:i A') . '</span></p>';

            file_put_contents('comments.txt', $comment, FILE_APPEND | LOCK_EX);
        } else {
            echo "<p>Error Code: " . $err . "</p>";
        }
    }

    read_comments();
    print_form($err);
}

print $pageStart;
process_form();
?>
