<?PHP
system('sudo raspistill -hf -w 512 -h 320 -o /var/www/imageembed.jpg -t 0');
$filename = "imageembed.jpg";
$handle = fopen($filename, "rb");
$contents = fread($handle, filesize($filename));
fclose($handle);
echo $contents;
?>
