from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson import ObjectId
import re


from models import User, Product, Request  

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class DashboardStatsResponse(BaseModel):
    success: bool
    stats: dict

class UsersListResponse(BaseModel):
    success: bool
    total: int
    page: int
    totalPages: int
    users: List[dict] 



@router.get("/stats", response_model=DashboardStatsResponse, status_code=status.HTTP_200_OK)
async def get_dashboard_stats():
    """
    GET /api/admin/stats (admin only)
    Note: Middleware/Dependencies should be used for admin authorization.
    """
    try:
        
        import asyncio
        
        total_users_task = User.find({"role": "user"}).count()
        total_products_task = Product.find_all().count()
        pending_requests_task = Request.find({"status": "pending"}).count()
        accepted_requests_task = Request.find({"status": "accepted"}).count()
        rejected_requests_task = Request.find({"status": "rejected"}).count()
        banned_users_task = User.find({"role": "user", "isBanned": True}).count()

        (
            total_users,
            total_products,
            pending_requests,
            accepted_requests,
            rejected_requests,
            banned_users
        ) = await asyncio.gather(
            total_users_task,
            total_products_task,
            pending_requests_task,
            accepted_requests_task,
            rejected_requests_task,
            banned_users_task
        )

        return {
            "success": True,
            "stats": {
                "totalUsers": total_users,
                "totalProducts": total_products,
                "pendingRequests": pending_requests,
                "acceptedRequests": accepted_requests,
                "rejectedRequests": rejected_requests,
                "bannedUsers": banned_users,
                "totalRequests": pending_requests + accepted_requests + rejected_requests,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=UsersListResponse, status_code=status.HTTP_200_OK)
async def get_all_users(
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100), 
    keyword: Optional[str] = None
):
    """
    GET /api/admin/users (admin only)
    """
    try:
        skip = (page - 1) * limit

        
        filter_query = {"role": "user"}
        
        if keyword:
           
            regex_query = {"$regex": keyword, "$options": "i"}
            filter_query["$or"] = [
                {"name": regex_query},
                {"email": regex_query}
            ]

        import asyncio
        
        
        users_task = User.find(filter_query).sort("-createdAt").skip(skip).limit(limit).to_list()
        total_task = User.find(filter_query).count()

        users, total = await asyncio.gather(users_task, total_task)
        
        total_pages = max(1, (total + limit - 1) // limit) 

        return {
            "success": True,
            "total": total,
            "page": page,
            "totalPages": total_pages,
            "users": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}/ban", status_code=status.HTTP_200_OK)
async def toggle_ban_user(user_id: str):
    """
    PUT /api/admin/users/:id/ban (admin only)
    """
    try:
        
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid User ID format")

        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if user.role == "admin":
            raise HTTPException(status_code=400, detail="Cannot ban an admin account")

       
        user.isBanned = not user.isBanned
        await user.save()

        return {
            "success": True,
            "message": "User has been banned" if user.isBanned else "User has been unbanned",
            "user": user
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
