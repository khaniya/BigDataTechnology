<?php
$unixtimestamp = time();
$c = array("XRP", "USD", "LTC", "INR", "JPY", "CNY");
$qrandom = rand(0,4);
$log = '';
for($i=0;$i<=$qrandom;$i++){
        $crandom = rand(0,5);
        $amount = rand(10556, 1215300)/100;
        $t_hash = strtoupper(md5($unixtimestamp));
        $log .= "{\"time\":$unixtimestamp,\"currency\":\"$c[$crandom]\", \"amount\":$amount,\"t_hash\"$
}
file_put_contents('/opt/kafka/data/ripple.api.json', $log, FILE_APPEND | LOCK_EX);
?>