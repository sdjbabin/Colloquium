<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "colloquium";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");


// Get data from POST request
$jobRole = $_POST['jobRole'];
$question = $_POST['question'];
$answer = $_POST['answer'];

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO warmup_responses (job_role, question, answer) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $jobRole, $question, $answer);

if ($stmt->execute()) {
    echo "Your answer has been saved successfully!";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
