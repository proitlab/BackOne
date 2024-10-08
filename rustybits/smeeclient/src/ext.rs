/*
 * Copyright (c)2021 ZeroTier, Inc.
 *
 * Use of this software is governed by the Business Source License included
 * in the LICENSE.TXT file in the project's root directory.
 *
 * Change Date: 2026-01-01
 *
 * On the date above, in accordance with the Business Source License, use
 * of this software will be governed by version 2.0 of the Apache License.
 */

use std::ffi::CStr;
use std::os::raw::c_char;

use crate::NetworkJoinedParams;
use crate::SmeeClient;

#[no_mangle]
pub extern "C" fn smee_client_new(
    temporal_url: *const c_char,
    namespace: *const c_char,
    task_queue: *const c_char,
) -> *mut SmeeClient {
    let url = unsafe {
        assert!(!temporal_url.is_null());
        CStr::from_ptr(temporal_url).to_str().unwrap()
    };

    let ns = unsafe {
        assert!(!namespace.is_null());
        CStr::from_ptr(namespace).to_str().unwrap()
    };

    let tq = unsafe {
        assert!(!task_queue.is_null());
        CStr::from_ptr(task_queue).to_str().unwrap()
    };

    match SmeeClient::new(url, ns, tq) {
        Ok(c) => Box::into_raw(Box::new(c)),
        Err(e) => {
            println!("error creating smee client instance: {}", e);
            std::ptr::null_mut()
        }
    }
}

#[no_mangle]
pub extern "C" fn smee_client_delete(ptr: *mut SmeeClient) {
    if ptr.is_null() {
        return;
    }
    let smee = unsafe {
        assert!(!ptr.is_null());
        Box::from_raw(&mut *ptr)
    };

    smee.shutdown();
}

#[no_mangle]
pub extern "C" fn smee_client_notify_network_joined(
    smee_instance: *mut SmeeClient,
    network_id: *const c_char,
    member_id: *const c_char,
) -> bool {
    let nwid = unsafe {
        assert!(!network_id.is_null());
        CStr::from_ptr(network_id).to_str().unwrap()
    };

    let mem_id = unsafe {
        assert!(!member_id.is_null());
        CStr::from_ptr(member_id).to_str().unwrap()
    };

    let smee = unsafe {
        assert!(!smee_instance.is_null());
        &mut *smee_instance
    };

    let params = NetworkJoinedParams::new(nwid, mem_id);

    match smee.notify_network_joined(params) {
        Ok(()) => true,
        Err(e) => {
            println!("error notifying network joined: {0}", e.to_string());
            false
        }
    }
}
