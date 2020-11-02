import request from 'umi-request';

import {buildFileFormData} from '@/utils/utils'
export async function queryCustomer(params) {
  return request('/api/xadmin/v1/customer', {
    params,
  });
}
export async function removeCustomer(params) {
  return request(`/api/xadmin/v1/customer/${params}`, {
    method: 'DELETE',
  });
}
export async function addCustomer(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/customer', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateCustomer(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/customer/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryCustomerVerboseName(params) {
  return request('/api/xadmin/v1/customer/verbose_name', {
    params,
  });
}
export async function queryCustomerListDisplay(params) {
  return request('/api/xadmin/v1/customer/list_display', {
    params,
  });
}
export async function queryCustomerDisplayOrder(params) {
  return request('/api/xadmin/v1/customer/display_order', {
    params,
  });
}


