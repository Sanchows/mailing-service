FROM mher/flower

COPY ./.wait-for-it.sh ./
ENTRYPOINT ["sh", "./.wait-for-it.sh"]