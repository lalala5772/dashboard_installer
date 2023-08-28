<?php
require_once 'db_config.php';

$query = "SELECT * FROM sensor";
$result = $mysqli->query($query);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = array(
            'id' => $row['id'],
            'date' => $row['date'],
            'soilMoist' => $row['soilMoist'],
            'temperature' => $row['temperature'],
            'state' => $row['state'],
            'imageUrl' => $row['imageUrl']

        );
    }
} 
$mysqli->close();

// JSON 형식으로 데이터 반환
header('Content-Type: application/json');
echo json_encode($data);
?>
