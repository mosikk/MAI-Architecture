workspace {
    name "Сайт заказа услуг"

    !identifiers hierarchical


    model {

        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь"

        profiru_system = softwareSystem "Сервис заказа услуг" {
            description "Сервис заказа услуг"

            
            user_service = container "User service" {
                description "Сервис управления пользователями"
            } 

            task_service = container "Task service" {
                description "Сервис управления услугами"
            } 
            
            order_service = container "Order service" {
                description "Сервис оформления заказов"
            } 

            group "Слой данных" {
                user_database = container "User database" {
                    description "База данных пользоватей"
                    technology "PostgreSQL 15"
                    tags "database"
                }

                user_cache = container "User cache" {
                    description "Кеш данных пользователей для ускорения аутентификации"
                    technology "Redis"
                    tags "database"
                }

                task_database = container "Tasks database" {
                    description "База данных услуг и заказов"
                    technology "MongoDB 5"
                    tags "database"
                }
            }

            user -> user_service "Регистрация и авторизация пользователей"
            user -> task_service "Добавление услуги"

            user_service -> user_cache "Получение и изменение данных о пользователях"
            user_service -> user_database "Получение и изменение данных о пользователях"
            user_service -> order_service "Получение заказа для пользователя"

			task_service -> task_database "Получение и изменение данных об услугах"

			order_service -> task_database "Получение и изменение данных о заказах"
            order_service -> task_service "Добавление услуг в заказ"   
        }

    }
    
    views {
        themes default

        properties {
            structurizr.tooltips true
        }

        systemContext profiru_system {
            autoLayout
            include *
        }

        container profiru_system {
            autoLayout
            include *
        }

        dynamic profiru_system "UC01" "Создание нового пользователя" {
            autoLayout
            user -> profiru_system.user_service "Создание пользователя (POST /user)"
            profiru_system.user_service -> profiru_system.user_database "Сохранение данных о пользователе" 
            profiru_system.user_service -> profiru_system.user_cache "Кэширование данных о пользователе" 
        }

        dynamic profiru_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> profiru_system.user_service "Поиск пользователя (GET /user)"
			profiru_system.user_service -> profiru_system.user_cache "Получение данных о пользователе из кэша"
            profiru_system.user_service -> profiru_system.user_database "Получение данных о пользователе из БД"
        }

        dynamic profiru_system "UC03" "Поиск пользователя по маске имени и фамилии" {
            autoLayout
            user -> profiru_system.user_service "Поиск пользователя"
            profiru_system.user_service -> profiru_system.user_database "Получение данных о пользователях, соответствующих маске"
        }

        dynamic profiru_system "UC04" "Создание услуги" {
            autoLayout
            user -> profiru_system.task_service "Создание новой услуги (POST /task)"
            profiru_system.task_service -> profiru_system.task_database "Сохранение данных об услуге"
        }

        dynamic profiru_system "UC05" "Получение списка услуг" {
            autoLayout
            user -> profiru_system.task_service "Получение списка всех усллуг (GET /task)"
            profiru_system.task_service -> profiru_system.task_database "Получение всех услуг из БД"
        }

        dynamic profiru_system "UC06" "Добавление услуг в заказ" {
            autoLayout
            user -> profiru_system.user_service "Создание заказа (POST /order)"
            profiru_system.user_service -> profiru_system.order_service "Добавление пользователя в заказ"
			profiru_system.order_service -> profiru_system.task_service "Добавление услуги в заказ"
			profiru_system.order_service -> profiru_system.task_database "Обновление информации о заказе в БД"
        }
        
        dynamic profiru_system "UC07" "Получение заказа для пользователя" {
            autoLayout
            user -> profiru_system.user_service "Получение информации о заказе (GET /order)"
            profiru_system.user_service -> profiru_system.order_service "Получение информации о заказе для пользователя (GET /order)"
			profiru_system.order_service -> profiru_system.task_database "Получение информации о заказе из БД"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}
