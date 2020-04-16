const express = require('express');
const app = express();

app.use(express.static('dashforge'));

app.get('/', (req, res) => {
    const fileName = '/template/sunfresh/index.html';
    res.sendFile(fileName, options, function (err) {
        if (err) {
            next(err)
        } else {
            console.log('Sent:', fileName)
        }
    })
});

app.listen(5070, () => console.log('sunfresh app listening on port 5070!'));
