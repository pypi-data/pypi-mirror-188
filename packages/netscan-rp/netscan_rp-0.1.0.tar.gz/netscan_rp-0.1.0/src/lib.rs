use pyo3::prelude::*;

use qscan::{QSPrintMode, QScanResult, QScanTcpConnectState, QScanType, QScanner};
use tokio::runtime::Runtime;


#[pyfunction]
fn scan(ip_list: &str, port_list: &str) -> PyResult<String>{

    let mut list_target_result:String = String::from("[");
    let mut found_port = false;

    let mut scanner = QScanner::new(ip_list, port_list);
    scanner.set_batch(500);
    scanner.set_timeout_ms(500);
    scanner.set_ntries(1);
    scanner.set_scan_type(QScanType::TcpConnect);
    scanner.set_print_mode(QSPrintMode::NonRealTime);

    let res: &Vec<QScanResult> = Runtime::new().unwrap().block_on(scanner.scan_tcp_connect());

    for r in res {
        if let QScanResult::TcpConnect(sa) = r {
            if sa.state == QScanTcpConnectState::Open {
                let target_return = (sa.target).to_string();
                let list_return   = target_return.split(":").collect::<Vec<_>>();

                list_target_result.push_str(",{\"IP\":\"");
                list_target_result.push_str(list_return[0]);
                list_target_result.push_str("\",\"PORT\":\"");
                list_target_result.push_str(list_return[1]);
                list_target_result.push_str("\"}");

                found_port = true;
            }
        }
    }

    list_target_result.push_str("]");
    list_target_result.replace_range(1..2, "");

    if found_port {
        Ok((list_target_result).to_string())
    } else {
        Ok(("[]").to_string())
    } 

    
}



#[pymodule]
fn netscan_rp(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan, m)?)?;
    Ok(())
}