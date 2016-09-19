<?php

// author: ringzero@0x557.org

/*
 $db =  new db_mysql('127.0.0.1', 'root', '', 'UTF8', 'test');

// update
// $where = sprintf('uid = %d AND appid IN (%s)', $uId, dimplode($appIds));

$data = array(
	'title' => 'change the title',
	'detail' => 'change the detail', 
	'begin_time' => '1');

$condition = array('id' => '71', 'title' => 'dsad');
$db->update('news', $data, $condition);


// insert
$data = array(
	'id' => NULL, 
	'title' => '74', 
	'detail' => 'dsad', 
	'begin_time' => '0');
$db->insert('news', $data);

// delete
$condition = array(
	'id' => '74', 
	'title' => 'dsad');
$db->delete('news', $condition);

// query
$query = $db->query('select * from u_members where uid < 100');
while ($members = $db->fetch_array($query)) {
	print_r($members);
}
*/

class db_mysql {
	
	private $dbhost;
	private $dbuser;
	private $dbpwd;
	private $dbname;
	private $dbcharset;
	
	function __construct($dbhost = DB_HOST, $dbuser = DB_USER, $dbpw = DB_PASSWORD, $dbcharset = DB_CHARSET, $dbname = DB_NAME){
		$this->dbhost = $dbhost;
		$this->dbuser = $dbuser;
		$this->dbpw = $dbpw;
		$this->dbcharset = $dbcharset;
		$this->dbname = $dbname;
		$this->connect();
	}
	
	function connect(){
		$link = @mysql_connect ( $this->dbhost, $this->dbuser, $this->dbpw ) or $this->halt( mysql_error() );
		mysql_select_db( $this->dbname, $link ) or $this->halt ( mysql_error() );
		mysql_query("SET NAMES '$this->dbcharset'");
	}
	
	function delete($table, $condition, $limit = 0) {
		if (empty ( $condition )) {
			$where = '1';
		} elseif (is_array ( $condition )) {
			$where = $this->implode_field_value ( $condition, ' AND ' );
		} else {
			$where = $condition;
		}
		$sql = "DELETE FROM " . $table . " WHERE $where " . ($limit ? "LIMIT $limit" : '');
		return $this->query ( $sql );
	}
	
	function insert($table, $data, $return_insert_id = false) {
		$sql = $this->implode_field_value ( $data );
		$return = $this->query ( "INSERT INTO $table SET $sql" );
		return $return_insert_id ? $this->insert_id () : $return;
	}
	
	function update($table, $data, $condition) {
		$sql = $this->implode_field_value ( $data );
		$where = '';
		if (empty ( $condition )) {
			$where = '1';
		} elseif (is_array ( $condition )) {
			$where = $this->implode_field_value ( $condition, ' AND ' );
		} else {
			$where = $condition;
		}
		$res = $this->query ( "UPDATE $table SET $sql WHERE $where" );
		return $res;
	}
	
	function fetch_array($query, $result_type = MYSQL_ASSOC) {
		return mysql_fetch_array ( $query, $result_type );
	}
	
	function fetch_first($sql) {
		return $this->fetch_array ( $this->query ( $sql ) );
	}
	
	function result_first($sql) {
		return $this->result ( $this->query ( $sql ), 0 );
	}
	
	function affected_rows() {
		return mysql_affected_rows();
	}
	
	function result($query, $row = 0) {
		$query = @mysql_result ( $query, $row );
		return $query;
	}
	
	function num_rows($query) {
		$query = mysql_num_rows ( $query );
		return $query;
	}
	
	function num_fields($query) {
		return mysql_num_fields ( $query );
	}
	
	function free_result($query) {
		return mysql_free_result ( $query );
	}
	
	function fetch_row($query) {
		$query = mysql_fetch_row ( $query );
		return $query;
	}
	
	function fetch_fields($query) {
		return mysql_fetch_field ( $query );
	}
	
	function version() {
		return mysql_get_server_info();
	}
	
	function close() {
		return mysql_close();
	}
	
	function implode_field_value($array, $glue = ',') {
		$sql = $comma = '';
		foreach ($array as $k => $v) {
			$sql .= $comma."`$k`='$v'";
			$comma = $glue;
		}
		return $sql;
	}
	
	public function halt($message = '', $sql = '') {
		echo "<!DOCTYPE html><html lang='en'><head><title>Error Page</title><style type='text/css'>::selection{ background-color: #E13300; color: white; }::moz-selection{ background-color: #E13300; color: white; }::webkit-selection{ background-color: #E13300; color: white; }body {	background-color: #fff;	margin: 40px;	font: 13px/20px normal Helvetica, Arial, sans-serif;	color: #4F5155;}a {	color: #003399;	background-color: transparent;	font-weight: normal;}h1 {	color: #444;	background-color: transparent;	border-bottom: 1px solid #D0D0D0;	font-size: 19px;	font-weight: normal;	margin: 0 0 14px 0;	padding: 14px 15px 10px 15px;}code {	font-family: Consolas, Monaco, Courier New, Courier, monospace;	font-size: 12px;	background-color: #f9f9f9;	border: 1px solid #D0D0D0;	color: #002166;	display: block;	margin: 14px 0 14px 0;	padding: 12px 10px 12px 10px;}#container {margin: 10px;border: 1px solid #D0D0D0;-webkit-box-shadow: 0 0 8px #D0D0D0;}p {	margin: 12px 15px 12px 15px;}</style></head><body><div id='container'><h1>ERROR INFO : $sql</h1><p>$message</p>	</div></body></html>";
		exit ();
	}
	
	function query($sql, $type = '') {
		if(!($query = mysql_query($sql))) $this->halt ( mysql_error(), $sql );
		return $query;
	}
}
?>