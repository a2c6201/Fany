window.onload = function () {
  document.getElementById("btn").onclick = async function () {
    // 位置情報を取得する
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);

    async function successCallback(position) {
      // 緯度を取得し画面に表示
      var latitude = await position.coords.latitude;
      // 経度を取得し画面に表示
      var longitude = await position.coords.longitude;
      let range = await document.getElementById("range").value;

      var json = JSON.stringify({
        lat: latitude,
        lng: longitude,
        range: range,
      });
      //Asyncによる非同期通信処理
      await fetch("/result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: json,
      });
      console.log(json);
      window.location.href = "/result";
    }

    function errorCallback(error) {
      alert("位置情報が取得できませんでした");
    }
  };
};
