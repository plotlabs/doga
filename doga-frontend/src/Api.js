import axios from "axios";

const Api = axios.create({
  baseURL: "http://0.0.0.0:8080/",
  headers: {
    "Content-Type": "application/json",
  },
});

Api.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.response.status === 401) {
      localStorage.clear();
      window.location.replace("/login");
    }
    if (error.response.status === 403) {
    }
    return Promise.reject(error);
  }
);
export const ApiApp = axios.create({
  baseURL: "http://0.0.0.0:8080/",
  headers: {
    "Content-Type": "application/json",
  },
});

ApiApp.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.response.status === 401) {
      localStorage.clear();
      window.location.replace("/login");
    }
    if (error.response.status === 403) {
    }
    return Promise.reject(error);
  }
);

export const ApiJwt = axios.create({
  baseURL: "http://0.0.0.0:8080/",
  headers: {
    "Content-Type": "application/json",
  },
});

export const ApiUpload = axios.create({
  baseURL: "http://0.0.0.0:8080/",
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export function setHeader(token) {
  Api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  ApiApp.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  ApiUpload.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function setDefaultBaseUrl(baseURL) {
  ApiApp.defaults.baseURL = baseURL;
}
export function setJwtHeader(token) {
  ApiJwt.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export const defaultQueryFn = async ({ queryKey }) => {
  try {
    const { data } =
      queryKey[1] === "jwt_info"
        ? await ApiJwt.get(queryKey[0])
        : queryKey[1] === "baseURL"
        ? await ApiApp.get(queryKey[0])
        : await Api.get(queryKey[0]);
    return data;
  } catch (error) {}
};

export const APIURLS = {
  login: "/admin/login",
  signup: "/admin/admin_profile",
  createDB: "/admin/dbinit",
  userInfo: "/admin/admin_profile/nishant@gmail.com",
  dashboardInfo: (section, filter) =>
    `/admin/dashboard/stats/${section}/${filter}`,
  appInfo: (app) => `/admin/dashboard/stats/${app}/all`,
  appStats: (app) => `/admin/dashboard/stats/app/${app}`,
  appDocs: (app) => `/admin/docs/${app}`,
  dbInfo: (db) => `/admin/dashboard/stats/db/${db}`,
  getDbConnections: "/admin/dbinit",
  getDbDefaults: "/admin/utils/defaults/db",
  getColumnTypes: "/admin/columntypes",
  getContentType: "/admin/content/types",
  getUserImages: "/admin/assets/list/image",
  getTableContent: ({ app, table }) => `/${app}/${table}/`,
  baseJwtLogin: ({ app, table }) => `/${app}/${table}/login`,
  postRegisterTableData: ({ app, table }) => `/${app}/${table}/register`,
  getUserCongif: () => `/admin/utils/aws/form/config`,
  getUserRdsCongif: () => `/admin/utils/aws/form/rds_config`,
  getUserEc2Congif: () => `/admin/utils/aws/form/ec2_config`,
  getTableContentById: ({ app, table, editDataId }) =>
    `/${app}/${table}/${editDataId}`,
  deleteTable: ({ app, table }) => `admin/content/types/${app}/${table}`,
  getForeignkey: "/admin/content/relations",
  exportApp: () => "/admin/export/local",
  awsExport: () => "/admin/export/aws",
  herokuExport: () => "/admin/export/heroku",
  emailNotify: () => "/admin/notify/email",
  smsNotify: () => "/admin/notify/sms",
  markAllNotifications: "/admin/info/markread/all",
  markIndividualNotifications: ({ id }) => `/admin/info/markread/${id}`,
  uploadImage: () => `/admin/assets/upload/image`,
  getNotifications: "/admin/info/allrequests",
};

export default Api;
