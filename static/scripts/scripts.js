function updatename(id, oldname) {
    console.log(id)
    const new_name = prompt("Enter new name for " + oldname);

    if (new_name != null || new_name != "") {
        let data = { "content": new_name };

        fetch("/update/" + id, {
            method: "POST",
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        }).then(res => {
            console.log("Request complete! response:", res);
        });
    }


}