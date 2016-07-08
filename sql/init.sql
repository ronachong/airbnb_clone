/* init.sql creates one user and one database for development and production each. */

CREATE USER 'airbnb_user_dev'@'%'
       IDENTIFIED BY 'wrdev';
CREATE USER 'airbnb_user_prod'@'localhost'
       IDENTIFIED BY 'wrprod';

CREATE DATABASE airbnb_dev
       DEFAULT CHARACTER SET utf8
       DEFAULT COLLATE utf8_general_ci;

CREATE DATABASE airbnb_prod
       DEFAULT CHARACTER SET utf8
       DEFAULT COLLATE utf8_general_ci;

/*
the following grant statements produces a warning, but should still be effective for current version of mysql:
| Warning | 1287 | Using GRANT statement to modify existing user's properties other than privileges is deprecated and will be removed in future release. Use ALTER USER statement for this operation. |
*/
GRANT ALL PRIVILEGES
      ON airbnb_dev.*
      TO 'airbnb_user_dev'@'%'
      IDENTIFIED BY 'wrdev';

GRANT ALL PRIVILEGES
      ON airbnb_prod.*
      TO 'airbnb_user_prod'@'localhost'
      IDENTIFIED BY 'wrprod';
