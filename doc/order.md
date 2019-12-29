## 买家下单

#### URL：
POST http://[address]/buyer/new_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
store_id | string | 商铺ID | N
books | class | 书籍购买列表 | N

books数组：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 初始库存，大于等于0 | N
count | string | 购买数量 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 下单成功
5XX | 买家用户ID不存在
5XX | 商铺ID不存在
5XX | 购买的图书不存在
5XX | 商品库存不足

##### Body:
```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单号，只有返回200时才有效 | N


## 买家付款

#### URL：
POST http://[address]/buyer/payment

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
order_id | string | 订单ID | N
password | string | 买家用户密码 | N 


#### Response

Status Code:

码 | 描述
--- | ---
200 | 付款成功
5XX | 账户余额不足
5XX | 无效参数
401 | 授权失败 


## 买家充值

#### URL：
POST http://[address]/buyer/add_funds

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
add_value | int | 充值金额，以分为单位 | N


Status Code:

码 | 描述
--- | ---
200 | 充值成功
401 | 授权失败
5XX | 无效参数

## 买家签收

#### URL：

POST http://[address]/buyer/confirm

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:

```json
{
  "user_id": "user_id",
  "password": "password",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述                 | 是否可为空 |
| -------- | ------ | -------------------- | ---------- |
| user_id  | string | 买家用户ID           | N          |
| password | string | 用户密码             | N          |
| order_id | int    | 订单号               | N          |


Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 签收成功 |
| 401  | 授权失败 |
| 5XX  | 无效参数 |

## 买家按条件查看历史订单

#### URL：

POST http://[address]/buyer/his_order



#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:

```json
{
  "user_id": "user_id",
  "password": "password",
  "type": "type",
  "context": "context"
}
```


##### 属性说明：

| key      | 类型   | 描述                 | 是否可为空 |
| -------- | ------ | -------------------- | ---------- |
| user_id  | string | 买家用户ID           | N          |
| password | string | 用户密码             | N          |
| type     | string | 筛选类型 | N          |
| context | int/string| 筛选条件 | N          |


#### Response

Status Code:

| 码   | 描述      |
| ---- | --------- |
| 200  | 查看成功  |
| 401  | 授权失败 |
| 5XX  | 无效参数 |

##### Body:

```
{
"order": [
  "[{"_id": {"$oid": "5e07ef105879d6913b732b32"}, "order_id": 58, "buyer": "jyh", "store": "test", "goods": [{"id": 1009273, "count": 1}, {"id": 1013801, "count": 2}], "total_amount": 300, "state": 0}]",
  "[{"_id": {"$oid": "5e07ef125879d6913b732b35"}, "order_id": 59, "buyer": "jyh", "store": "test", "goods": [{"id": 1009273, "count": 1}, {"id": 1013801, "count": 2}], "total_amount": 300, "state": 0}]"
],
}
```

##### 属性说明：

| 变量名 | 类型 | 描述                           | 是否可为空 |
| ------ | ---- | ------------------------------ | ---------- |
| orders | array | 历史订单列表状态码为200时有效) | N          |

orders数组：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| order_id | int | 订单号 | N          |
| buyer | string | 买家 | N          |
| store | string | 店铺 | N          |
| goods | array | 购买商品列表 | N          |
| total_amount | int | 订单总额 | N          |
| state | int | 当前订单状态 | N          |


订单状态：

|  状态表示  | 状态描述       |
| -------- | ---------- |
| 0 | 未付款 |
| 1 | 已付款 |
| 2 | 已取消 | 
| 3 | 已完成 |
| 4 | 已发货 |


## 买家取消订单

#### URL：

POST http://[address]/buyer/cancel_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:

```json
{
  "user_id": "user_id",
  "password": "password",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| password | string | 用户密码   | N          |
| order_id | string | 订单号     | N          |


Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 取消成功 |
| 401  | 授权失败 |
| 5XX  | 无效参数 |

## 卖家发货

#### URL：

POST http://[address]/buyer/deliver

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:

```json
{
  "user_id": "user_id",
  "password": "password",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 卖家用户ID | N          |
| password | string | 用户密码   | N          |
| order_id | string | 订单号     | N          |


Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 发货成功 |
| 401  | 授权失败 |
| 5XX  | 无效参数 |