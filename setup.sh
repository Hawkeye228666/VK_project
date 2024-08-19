#!/bin/bash
#chmod +x /opt/tarantool/setup.sh
# Остановка выполнения скрипта при ошибке
set -e

# Проверка на существование файла tt.yaml
if [ -f "tt.yaml" ]; then
    echo "tt.yaml уже существует. Пропускаем команду tt init."
else
    # Инициализация окружения Tarantool, если файла нет
    tt init
fi

# Создание директории для инстанса
mkdir -p instances.enabled/create_db

# Создание файла instances.yml
cat <<EOL > instances.enabled/create_db/instances.yml
instance001:
EOL

# Создание файла config.yaml
cat <<EOL > instances.enabled/create_db/config.yaml
credentials:
  users:
    sampleuser:
      password: '123456'
      privileges:
      - permissions: [ read, write ]
        spaces: [ kv_store ]
      - permissions: [ execute ]
        functions: [  ]
groups:
  group001:
    replicasets:
      replicaset001:
        instances:
          instance001:
            iproto:
              listen:
              - uri: '127.0.0.1:3301'
app:
  file: 'init.lua'

EOL

cat <<EQL > instances.enabled/create_db/init.lua
box.cfg {
    listen = '0.0.0.0:3301',
    log_level = 5
}

if not box.space.kv_store then
    local kv_store = box.schema.space.create('kv_store', {
        if_not_exists = true
    })

    kv_store:create_index('primary', {
        type = 'hash',
        parts = {1, 'string'},
        if_not_exists = true
    })
end

EQL

tt start create_db





