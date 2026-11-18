import React from "react";

function ReconciliationTable({ results }) {
  if (!results || results.length === 0) {
    return <p className="empty-message">No reconciliation results found.</p>;
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>System A Amount</th>
            <th>System B Amount</th>
            <th>System A Date</th>
            <th>System B Date</th>
            <th>Status</th>
            <th>Difference</th>
          </tr>
        </thead>

        <tbody>
          {results.map((item, index) => (
            <tr key={item.id || index}>
              <td>{item.transaction_id || "-"}</td>
              <td>{item.system_a_amount ?? "-"}</td>
              <td>{item.system_b_amount ?? "-"}</td>
              <td>{item.system_a_date || "-"}</td>
              <td>{item.system_b_date || "-"}</td>
              <td>
                <span
                  className={`status ${
                    item.status?.toLowerCase() || "unknown"
                  }`}
                >
                  {item.status || "UNKNOWN"}
                </span>
              </td>
              <td>{item.difference ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReconciliationTable;