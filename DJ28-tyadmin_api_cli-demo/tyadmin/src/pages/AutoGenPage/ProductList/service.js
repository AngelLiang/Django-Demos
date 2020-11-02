import request from 'umi-request';

import {buildFileFormData} from '@/utils/utils'
export async function queryProduct(params) {
  return request('/api/xadmin/v1/product', {
    params,
  });
}
export async function removeProduct(params) {
  return request(`/api/xadmin/v1/product/${params}`, {
    method: 'DELETE',
  });
}
export async function addProduct(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/product', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateProduct(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/product/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryProductVerboseName(params) {
  return request('/api/xadmin/v1/product/verbose_name', {
    params,
  });
}
export async function queryProductListDisplay(params) {
  return request('/api/xadmin/v1/product/list_display', {
    params,
  });
}
export async function queryProductDisplayOrder(params) {
  return request('/api/xadmin/v1/product/display_order', {
    params,
  });
}


