const express = require('express');
const path = require('path');
const app = express();

// 정적 파일 경로 설정
map_app.use(express.static(path.join(__dirname, 'public')));

map_app.get('/roadview_line', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'roadview_line.html'));
});

const PORT = 3000;
map_app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
