<?php
// login.php

session_start(); // Start the session to store user data

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve username and password from the form
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Database connection
    $conn = new mysqli('localhost', 'root', '', 'user_auth');

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Prepare the SQL query to prevent SQL injection
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    // Check if the user exists
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        // Verify the password
        if (password_verify($password, $user['password'])) {
            // Set session variables for logged-in user
            $_SESSION['username'] = $user['username'];
            // Redirect to the chatbot page
            header("Location: chatbot.html");
            exit();
        } else {
            // Invalid password
            echo "Invalid password!";
        }
    } else {
        // User not found
        echo "No user found with that username!";
    }

    // Close connections
    $stmt->close();
    $conn->close();
}
?>
