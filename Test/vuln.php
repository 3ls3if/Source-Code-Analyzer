    <?php
    $file = fopen('test.txt', 'w');
    $content = file_get_contents('http://example.com');
    $result = system('ls -la');
    $data = unserialize($_POST['data']);
    $conn = new mysqli('localhost', 'user', 'pass', 'database');
    ?>
