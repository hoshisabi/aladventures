---
layout: page
title: AL Adventures
datatable: true
---

{% assign dc_adventures = site.data.SJ-DC %}

<div class="al-table">
<table class="sortable">
  <thead>
    <tr>
      <th>Code</th>
      <th>Title</th>
      <th>Authors</th>
      <th>URL</th>
    </tr>
  </thead>
  <tbody>
    {% for item in dc_adventures %}
      <tr>
        <td>{{ item.code }}</td>
        <td>{{ item.title }}</td>
        <td>{{ item.authors | join: ", " }}</td>
        <td><a href="{{ item.url }}">{{ item.url }}</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>
</div>


<link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.css" rel="stylesheet" />
<link href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css" rel="stylesheet" />

<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.js"></script>
<script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
<script>
  $(document).ready(function () {
    $("#al-table > table").DataTable();
  });
</script>